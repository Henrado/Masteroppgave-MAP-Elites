import numpy as np

def shortestAngleFloat(from_deg: float, to_deg: float) -> float:
        diff = from_deg - to_deg
        while (diff >  180): diff -= 2*180
        while (diff < -180): diff += 2*180
        return diff

def basicFitness(x_cur: float,y_cur: float,yaw_cur: float, count_collide=None):
    """
    En basic fitnessfunksjon som finner ut hvor langt unna i vinkel den er i forhold til det den skulle ha hvert

    Parameters:
        x_cur (float) Hvor langt i x retning den er 
        y_cur (float) Hvor langt i y retning den er
        yaw_cur (float) Hvor mye yaw den har vrid seg i grader
        count_collide (int) Antall ganger den har kollidert med bakken 

    Return: 
        fitness (float) Hvor langt unna den var [0-1], minimering er bedre
    """
    wanted_yaw = np.arctan2(x_cur, y_cur)
    wanted_yaw = np.rad2deg(wanted_yaw)%360
    yaw_cur = yaw_cur%360
    a=abs(shortestAngleFloat(yaw_cur, wanted_yaw))
    return np.interp(a, [0, 180], [0, 1])


if __name__ == "__main__":
    basicFitness(-1,-1,45.0)