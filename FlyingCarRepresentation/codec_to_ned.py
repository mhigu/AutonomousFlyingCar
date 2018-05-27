import utm
import numpy as np

def global_to_local(global_position, global_home):
    
    # Get easting and northing of global_home
    # Get easting and northing of global_position
    # Create local_position from global and home positions                                     

    (east_home, north_home, _, _) = utm.from_latlon(global_home[1], global_home[0])
    (east, north, _, _) = utm.from_latlon(global_position[1], global_position[0])

    local_position = np.array([north - north_home, east - east_home, -global_position[2]])
    
    return local_position

def local_to_global(local_position, global_home):
    
    # get easting, northing, zone letter and number of global_home
    # get (lat, lon) from local_position and converted global_home
    # Create global_position of (lat, lon, alt)
    
                               
    (east_home, north_home, zone_number, zone_letter) = utm.from_latlon(global_home[1], global_home[0])
    (lat, lon) = utm.to_latlon(east_home + local_position[1], north_home + local_position[0], zone_number, zone_letter)
    
    return np.array([lon, lat, -local_position[2]])

if __name__ == '__main__':
    np.set_printoptions(precision=2)

    geodetic_current_coordinates = [-122.079465, 37.393037, 30]
    geodetic_home_coordinates = [-122.108432, 37.400154, 20]

    local_coordinates_NED = global_to_local(geodetic_current_coordinates, geodetic_home_coordinates)

    print(local_coordinates_NED)
    # Should print [ -764.96  2571.59   -10.  ]

    np.set_printoptions(precision=6)
    NED_coordinates =[25.21, 128.07, -30.]

    # convert back to global coordinates
    geodetic_current_coordinates = local_to_global(NED_coordinates, geodetic_home_coordinates)

    print(geodetic_current_coordinates)
    # Should print [-122.106982   37.40037    50.      ]