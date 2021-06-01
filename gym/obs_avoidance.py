import numpy as np
from argparse import Namespace

def nearest_point_on_trajectory(point, trajectory):
    diffs = trajectory[1:,:] - trajectory[:-1,:]
    l2s   = diffs[:,0]**2 + diffs[:,1]**2
    # this is equivalent to the elementwise dot product
    dots = np.empty((trajectory.shape[0]-1, ))
    for i in range(dots.shape[0]):
        dots[i] = np.dot((point - trajectory[i, :]), diffs[i, :])
    t = dots / l2s
    t[t<0.0] = 0.0
    t[t>1.0] = 1.0
    projections = trajectory[:-1,:] + (t*diffs.T).T
    dists = np.empty((projections.shape[0],))
    for i in range(dists.shape[0]):
        temp = point - projections[i]
        dists[i] = np.sqrt(np.sum(temp*temp))
    min_dist_segment = np.argmin(dists)
    return projections[min_dist_segment], dists[min_dist_segment], t[min_dist_segment], min_dist_segment

class TempPath:
    def __init__(self,conf):
        self.conf = conf
        self.load_waypoints(conf)
        
    def load_waypoints(self, conf):
        # load wps
        temp = np.loadtxt(conf.wpt_path, delimiter=conf.wpt_delim, skiprows=conf.wpt_rowskip)
        self.global_wps = np.vstack((temp[:,self.conf.wpt_xind], temp[:,self.conf.wpt_yind])).T
    
    def input_poses(self, current_wps, obs_poses):
        self.current_wps = current_wps
        self.obs_poses = obs_poses
    
    def create_obs_map(self):
        
        _dists = []
        _idxs = []
        
        for i in range(len(self.obs_poses)):
            _, temp_dists, _, temp_idx = nearest_point_on_trajectory(self.obs_poses[i],self.global_wps)
            _dists.append(temp_dists)
            _idxs.append(temp_idx)
        
        goal_idx = _idxs[np.argmax(_dists)]
        
        # print(_dists)
        # print(_idxs)
        # print(goal_idx)
    
