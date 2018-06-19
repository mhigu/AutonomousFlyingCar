## Project: 3D Motion Planning README/WRITEUP
![Quad Image](./misc/enroute.png)

---


# Required Steps for a Passing Submission:
1. Load the 2.5D map in the colliders.csv file describing the environment.
2. Discretize the environment into a grid or graph representation.
3. Define the start and goal locations.
4. Perform a search using A* or other search algorithm.
5. Use a collinearity test or ray tracing method (like Bresenham) to remove unnecessary waypoints.
6. Return waypoints in local ECEF coordinates (format for `self.all_waypoints` is [N, E, altitude, heading], where the drone’s start location corresponds to [0, 0, 0, 0].
7. Write it up.
8. Congratulations!  Your Done!

This project obey to this [Rubric](https://review.udacity.com/#!/rubrics/1534/view) Points.


---
### Writeup

Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

#### Explain the functionality of what's provided in `motion_planning.py` and `planning_utils.py`

##### 1. what's different about `motion_planning.py` from the `backyard_flyer_solution.py`

In `backyard_flyer_solution.py`, the waypoints is set to move as square(just straight to north or east) like this [this line shows](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/backyard_flyer_solution.py#L72-L75)

But in `motion_planning.py`, the waypoints(path) is calculated by [a_start()](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/planning_utils.py#L91) function.

And diagonal direction movement is not allowed in [Action](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/planning_utils.py#L45-L65) so `motion_planning.py` is executed, the behavior is going be a jerky path of waypoints to the northeast for about 10 m then land.

##### 2. how the functions provided in `planning_utils.py` work

`motion_planning.py` is using these function in `planning_utils.py` for each usage described bellow.

function name | how this function used
--- | --- 
create_grid() | [to create grid](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/motion_planning.py#L136) for data `colliders.csv` gives   
heuristic() | [to give heuristic](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/motion_planning.py#L150) for a_star search  
a_star() | [to calculate waypoints](https://github.com/udacity/FCND-Motion-Planning/blob/590a4c12b9ec76295a396d8c87a34f149176c119/motion_planning.py#L150) drone fly  


### Implementing Your Path Planning Algorithm

#### 1. Set your global home position
Read the first line of the csv file, extract lat0 and lon0 as floating point values and use the self.set_home_position() method to set global home.

https://github.com/mhigu/Udacity_FlyingCarND/blob/5641aed04a466da518e60a9f7dca43f81c26e1e9/projects/FCND-Motion-Planning/motion_planning.py#L128-L133

And here is a lovely picture of our downtown San Francisco environment from above!
![Map of SF](./misc/map.png)

#### 2. Set your current local position
Determine local position relative to global home using global_to_local() function. 

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/motion_planning.py#L137

I don't retrieve current global position and global position, because there is global_position attribute in class so just path it to global_to_local() function.
The return value passed to `current_local_position` variable.

#### 3. Set grid start position from local position
Set start position from local position in here.

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/motion_planning.py#L152

Just retrieve north, east coordinate value from `current_local_position` I defined before. This part was little hard because I can't figure out what is representing local position value and how it should be handled in. So I had to read source code deeper and write down what is done inside source code... But anyway I found out that is same value as colliders.csv file has. 

#### 4. Set grid goal position from geodetic coords
Set goal position in here.

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/motion_planning.py#L157

This part also difficult for me first as I described above due to confusion for local position. But once I got that make sense to me.  

#### 5. Modify A* to include diagonal motion (or replace A* altogether)
Modify code in planning_utils() to update the A* implementation to include diagonal motions on the grid that have a cost of sqrt(2).

[Action Definition]

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/planning_utils.py#L46-L70

Just define each diagonal movement. This part was easy.  

[Action Validation]

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/planning_utils.py#L73-L101

Action validation had a bug first that plan removes Action twice. Then I debugged, and fixed condition for that then it worked! 

#### 6. Cull waypoints 
Use collinearity test to prune path of unnecessary waypoints using determinant.

https://github.com/mhigu/Udacity_FlyingCarND/blob/66c901676816da47bd032c035c77732dbc6bc207/projects/FCND-Motion-Planning/planning_utils.py#L164-L167

Pruning path is a little tricky for me because making epsilon(error value) for determinant bigger, then my drone stack in middle of the waypoint. So I had to adjust that value.
This have to be solved by medial axis approach and graph approach I think. But I don't have enough time for now so leave it as FIXME and I'll come back when I got some more time later.  

### Execute the flight
#### 1. Does it work?

```bash
git https://github.com/mhigu/Udacity_FlyingCarND.git
cd projects/FCND-Motion-Planning

# up simulator!
# and exexute python script
# lat/lon argument is optional for custom goal designation.
python motion_planning.py [--lat xxx --lon yyy] 
```

It works!
