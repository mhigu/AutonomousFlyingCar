# Estimation Project #

In this project, I will be developing the estimation portion of the controller used in the CPP simulator.  

![top](images/predict-slow-drift.png)


## The Tasks ##

Project outline:

 - [Step 1: Sensor Noise](#step-1-sensor-noise)
 - [Step 2: Attitude Estimation](#step-2-attitude-estimation)
 - [Step 3: Prediction Step](#step-3-prediction-step)
 - [Step 4: Magnetometer Update](#step-4-magnetometer-update)
 - [Step 5: Closed Loop + GPS Update](#step-5-closed-loop--gps-update)
 - [Step 6: Adding Your Controller](#step-6-adding-your-controller)



### Step 1: Sensor Noise ###

For the controls project, the simulator was working with a perfect set of sensors, meaning none of the sensors had any noise.  
The first step to adding additional realism to the problem, and developing an estimator, is adding noise to the quad's sensors. 
For the first step, I will collect some simulated noisy sensor data and estimate the standard deviation of the quad's sensor.

1. Run the simulator in the same way as you have before
2. Choose scenario `06_NoisySensors`.  In this simulation, the interest is to record some sensor data on a static quad, so you will not see the quad move.  You will see two plots at the bottom, one for GPS X position and one for The accelerometer's x measurement.  The dashed lines are a visualization of a single standard deviation from 0 for each signal. The standard deviations are initially set to arbitrary values (after processing the data in the next step, you will be adjusting these values).  If they were set correctly, we should see ~68% of the measurement points fall into the +/- 1 sigma bound.  When you run this scenario, the graphs you see will be recorded to the following csv files with headers: `config/log/Graph1.txt` (GPS X data) and `config/log/Graph2.txt` (Accelerometer X data).
3. Process the logged files to figure out the standard deviation of the the GPS X signal and the IMU Accelerometer X signal.
4. Plug in your result into the top of `config/6_Sensornoise.txt`.  Specially, set the values for `MeasuredStdDev_GPSPosXY` and `MeasuredStdDev_AccelXY` to be the values you have calculated.
5. Run the simulator. If your values are correct, the dashed lines in the simulation will eventually turn green, indicating you’re capturing approx 68% of the respective measurements (which is what we expect within +/- 1 sigma bound for a Gaussian noise model)


For step 4, I use pandas `read_csv()` and `std()` method for `DataFrame` for each csv file(config/log/Graph1.txt, config/log/Graph2.txt).

And the sample is like this

```python
import pandas as pd
g1 = pd.read_csv('/Users/mhigu/dev/GitHub/Udacity_FlyingCarND/projects/FCND-Estination-CPP/config/log/Graph1.txt')
g1.std()
# you can use `g1.std(ddof=False)` when you have big data
``` 

And output become like this.

```text
time           1.009937
Quad.GPS.X     0.612126
dtype: float64
```

And use this value for each. 

***Success criteria:*** *standard deviations should accurately capture the value of approximately 68% of the respective measurements.*



### Step 2: Attitude Estimation ###

Now let's look at the first step to our state estimation: including information from our IMU.  
In this step, I will be improving the complementary filter-type attitude filter with a better rate gyro attitude integration scheme.

1. Run scenario `07_AttitudeEstimation`.  For this simulation, the only sensor used is the IMU and noise levels are set to 0 (see `config/07_AttitudeEstimation.txt` for all the settings for this simulation).  There are two plots visible in this simulation.
   - The top graph is showing errors in each of the estimated Euler angles.
   - The bottom shows the true Euler angles and the estimates.
Observe that there’s quite a bit of error in attitude estimation.

2. In `QuadEstimatorEKF.cpp`, I will see the function `UpdateFromIMU()` contains a complementary filter-type attitude filter.  
To reduce the errors in the estimated attitude (Euler Angles), implement a better rate gyro attitude integration scheme.  
I should be able to reduce the attitude errors to get within 0.1 rad for each of the Euler angles, as shown in the screenshot below.

![attitude example](images/attitude-screenshot.png)

In the screenshot above the attitude estimation using linear scheme (left) and using the improved nonlinear scheme (right). 
Note that Y axis on error is much greater on left.

**Hint: see section 7.1.2 of [Estimation for Quadrotors](https://www.overleaf.com/read/vymfngphcccj) for a refresher on a good non-linear complimentary filter for attitude using quaternions.**

As hint above shows, the equation apply high pass filter and low pass filter for accelerometer and gyro sensor.
Because of this, estimator will be robust to 

* short term noise
* susceptible to drift

But the implementation provided linear one. So it's necessary to implement non-linear one.

First, I need to translate body frame sensor value to world frame value using rotation matrix.

![rotation matrix](images/rotation-matrix.png)

After translation, we integrate prediction value.

```cpp
float predictedRoll = rollEst + dtIMU * euler_dot.x;
float predictedPitch = pitchEst + dtIMU * euler_dot.y;
ekfState(6) = ekfState(6) + dtIMU * euler_dot.z;	// yaw
```

Then I got this

![result2](images/res2.gif)

***Success criteria:*** *Your attitude estimator needs to get within 0.1 rad for each of the Euler angles for at least 3 seconds.*


### Step 3: Prediction Step ###

In this step you will be implementing the prediction step of your filter.


1. Run scenario `08_PredictState`.  This scenario is configured to use a perfect IMU (only an IMU). Due to the sensitivity of double-integration to attitude errors, we've made the accelerometer update very insignificant (`QuadEstimatorEKF.attitudeTau = 100`).  The plots on this simulation show element of your estimated state and that of the true state.  At the moment you should see that your estimated state does not follow the true state.
2. In `QuadEstimatorEKF.cpp`, implement the state prediction step in the `PredictState()` functon. If you do it correctly, when you run scenario `08_PredictState` you should see the estimator state track the actual state, with only reasonably slow drift, as shown in the figure below:
![predict drift](images/predict-slow-drift.png)

3. Now let's introduce a realistic IMU, one with noise.  Run scenario `09_PredictionCov`. You will see a small fleet of quadcopter all using your prediction code to integrate forward. You will see two plots:
   - The top graph shows 10 (prediction-only) position X estimates
   - The bottom graph shows 10 (prediction-only) velocity estimates
You will notice however that the estimated covariance (white bounds) currently do not capture the growing errors.
4. In `QuadEstimatorEKF.cpp`, calculate the partial derivative of the body-to-global rotation matrix in the function `GetRbgPrime()`.  Once you have that function implement, implement the rest of the prediction step (predict the state covariance forward) in `Predict()`.

**Hint: see section 7.2 of [Estimation for Quadrotors](https://www.overleaf.com/read/vymfngphcccj) for a refresher on the the transition model and the partial derivatives you may need**

**Hint: When it comes to writing the function for GetRbgPrime, make sure to triple check you've set all the correct parts of the matrix.**

**Hint: recall that the control input is the acceleration!**

5. Run your covariance prediction and tune the `QPosXYStd` and the `QVelXYStd` process parameters in `QuadEstimatorEKF.txt` to try to capture the magnitude of the error you see. Note that as error grows our simplified model will not capture the real error dynamics (for example, specifically, coming from attitude errors), therefore  try to make it look reasonable only for a relatively short prediction period (the scenario is set for one second).  A good solution looks as follows:

![good covariance](images/predict-good-cov.png)

Looking at this result, you can see that in the first part of the plot, our covariance (the white line) grows very much like the data.

If we look at an example with a `QPosXYStd` that is much too high (shown below), we can see that the covariance no longer grows in the same way as the data.

![bad x covariance](images/bad-x-sigma.PNG)

Another set of bad examples is shown below for having a `QVelXYStd` too large (first) and too small (second).  As you can see, once again, our covariances in these cases no longer model the data well.

![bad vx cov large](images/bad-vx-sigma.PNG)

![bad vx cov small](images/bad-vx-sigma-low.PNG)

***Success criteria:*** *This step doesn't have any specific measurable criteria being checked.*


#### `PredictState()`

In `PredictState()` function, I implement dead reckoning from lesson Notebook(Dead Reckoning In 3D).

The code look like this.

```cpp
// Dead Reckoning

predictedState(0) = curState(0) + curState(3) * dt;
predictedState(1) = curState(1) + curState(4) * dt;
predictedState(2) = curState(2) + curState(5) * dt;

// Convert body frame to the inertial frame
V3F acc_int = attitude.Rotate_BtoI(accel);

predictedState(3) = curState(3) + acc_int.x * dt;
predictedState(4) = curState(4) + acc_int.y * dt;
predictedState(5) = curState(5) + acc_int.z * dt - CONST_GRAVITY * dt;
```

And this code reduce error.

![predictState](images/predictState.png) 

#### `GetRbgPrime()`

In `GetRbgPrime()` function, I implement calculating the partial derivative of the body-to-global rotation matrix.

As [this document](https://www.overleaf.com/read/vymfngphcccj#/54894644/) describe in 7.2 Transition Model,

![Rgb-matrix](images/Rgb-prime-matrix.png)   

And this code look like this,

```cpp
RbgPrime(0,0) = -(cos(theta) * sin(psi));
RbgPrime(0,1) = -(sin(phi) * sin(theta) * sin(psi)) - (cos(phi) * cos(psi));
RbgPrime(0,2) = -(cos(phi) * sin(theta) * sin(psi)) + sin(phi) * cos(psi);
RbgPrime(1,0) = cos(theta) * cos(psi);
RbgPrime(1,1) = sin(phi) * sin(theta) * cos(psi) - cos(phi) * sin(psi);
RbgPrime(1,2) = cos(phi) * sin(theta) * cos(psi) + sin(phi) * sin(psi);
RbgPrime(2,0) = 0;
RbgPrime(2,1) = 0;
RbgPrime(2,2) = 0;
```

#### `Predict()`

Predict the current covariance forward by dt using the current accelerations and body rates as input using `getRbgPrime()` method implemented in previous step
and g pime function like this.

![g-prime](images/g-prime.png)


```cpp
gPrime(0,3) = dt;
gPrime(1,4) = dt;
gPrime(2,5) = dt;
gPrime(3, 6) = (RbgPrime(0) * accel).sum() * dt;
gPrime(4, 6) = (RbgPrime(1) * accel).sum() * dt;
gPrime(5, 6) = (RbgPrime(2) * accel).sum() * dt;
ekfCov = gPrime * ekfCov * gPrime.transpose() + Q;
```

The result is this

![res3-2](images/res3-2.png)

### Step 4: Magnetometer Update ###

Up until now we've only used the accelerometer and gyro for our state estimation.  
In this step, I will be adding the information from the magnetometer to improve filter's performance in estimating the vehicle's heading.

1. Run scenario `10_MagUpdate`.  This scenario uses a realistic IMU, but the magnetometer update hasn’t been implemented yet. As a result, you will notice that the estimate yaw is drifting away from the real value (and the estimated standard deviation is also increasing).  Note that in this case the plot is showing you the estimated yaw error (`quad.est.e.yaw`), which is drifting away from zero as the simulation runs.  You should also see the estimated standard deviation of that state (white boundary) is also increasing.
2. Tune the parameter `QYawStd` (`QuadEstimatorEKF.txt`) for the QuadEstimatorEKF so that it approximately captures the magnitude of the drift, as demonstrated here:
![mag drift](images/mag-drift.png)
3. Implement magnetometer update in the function `UpdateFromMag()`.  Once completed, you should see a resulting plot similar to this one:
![mag good](images/mag-good-solution.png)

***Success criteria:*** *Your goal is to both have an estimated standard deviation that accurately captures the error and maintain an error of less than 0.1rad in heading for at least 10 seconds of the simulation.*

**Hint: after implementing the magnetometer update, you may have to once again tune the parameter `QYawStd` to better balance between the long term drift and short-time noise from the magnetometer.**

**Hint: see section 7.3.2 of [Estimation for Quadrotors](https://www.overleaf.com/read/vymfngphcccj) for a refresher on the magnetometer update.**

#### `UpdateFromMag()`

We get a sensor value from the magnetometer reporting yaw in the global frame.

![yaw_magnetometer](images/magnetometer-1.png)

And this is liner so the derivative is a matrix of zeros and ones.

![yaw_derivative](images/magnetometer-2.png)

So I implement this code.

```cpp
hPrime(0, 6) = 1;
zFromX(0) = ekfState(6);

float diff = magYaw - zFromX(0);
if ( diff > F_PI ) {
  zFromX(0) += 2.f*F_PI;
} else if ( diff < -F_PI ) {
  zFromX(0) -= 2.f*F_PI;
}
```

And the result is

![res4](images/res4.png)

### Step 5: Closed Loop + GPS Update ###

1. Run scenario `11_GPSUpdate`.  At the moment this scenario is using both an ideal estimator and and ideal IMU.  Even with these ideal elements, watch the position and velocity errors (bottom right). As you see they are drifting away, since GPS update is not yet implemented.

2. Let's change to using your estimator by setting `Quad.UseIdealEstimator` to 0 in `config/11_GPSUpdate.txt`.  Rerun the scenario to get an idea of how well your estimator work with an ideal IMU.

3. Now repeat with realistic IMU by commenting out these lines in `config/11_GPSUpdate.txt`:
```
#SimIMU.AccelStd = 0,0,0
#SimIMU.GyroStd = 0,0,0
```

4. Tune the process noise model in `QuadEstimatorEKF.txt` to try to approximately capture the error you see with the estimated uncertainty (standard deviation) of the filter.

5. Implement the EKF GPS Update in the function `UpdateFromGPS()`.

6. Now once again re-run the simulation.  Your objective is to complete the entire simulation cycle with estimated position error of < 1m (you’ll see a green box over the bottom graph if you succeed).  You may want to try experimenting with the GPS update parameters to try and get better performance.

***Success criteria:*** *Your objective is to complete the entire simulation cycle with estimated position error of < 1m.*

**Hint: see section 7.3.1 of [Estimation for Quadrotors](https://www.overleaf.com/read/vymfngphcccj) for a refresher on the GPS update.**


#### UpdateFromGPS()

We get position and velocity from the GPS. 
We considered using heading from the GPS, but this does not take into account the drone’s orientation, 
only the direction of travel. Hence we are removing it from the observation.

![gps-1](images/gps-1.png)

Then the measurement model is

![gps-2](images/gps-2.png)

Then the partial derivative is the identity matrix,

![gps-3](images/gps-3.png)

And this will be a simple code like this.

```cpp
zFromX(0) = ekfState(0);
zFromX(1) = ekfState(1);
zFromX(2) = ekfState(2);
zFromX(3) = ekfState(3);
zFromX(4) = ekfState(4);
zFromX(5) = ekfState(5);

hPrime(0, 0) = 1;
hPrime(1, 1) = 1;
hPrime(2, 2) = 1;
hPrime(3, 3) = 1;
hPrime(4, 4) = 1;
hPrime(5, 5) = 1;
```

And result is like this.

![res5](images/res5.png)

At this point, congratulations on having a working estimator!

### Step 6: Adding Your Controller ###

Up to this point, we have been working with a controller that has been relaxed to work with an estimated state instead of a real state.  
So now, you will see how well your controller performs and de-tune your controller accordingly.

The result is like this 

![res6](images/res6.png)

And this result is not good enough and I need dig more deeper about the parameters after I graduate this entire course!!