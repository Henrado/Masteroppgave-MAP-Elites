import numpy as np

def shortestAngleFloat(from_deg: float, to_deg: float) -> float:
        diff = from_deg - to_deg
        while (diff >  180): diff -= 2*180
        while (diff < -180): diff += 2*180
        return diff

def basicFitness(x_cur: float,y_cur: float,yaw_cur: float, count_collide:int=0) -> np.float64:
    """
    En basic fitnessfunksjon som finner ut hvor langt unna i vinkel den er i forhold til det den skulle ha hvert

    Parameters:
        x_cur (float) Hvor langt i x retning den er 
        y_cur (float) Hvor langt i y retning den er
        yaw_cur (float) Hvor mye yaw den har vrid seg i grader
        count_collide (int) Antall ganger den har kollidert med bakken 

    Return: 
        fitness (float) Hvor langt unna den var [0-1], større er bedre
    """
    #wanted_yaw = np.arctan2(x_cur, y_cur)
    wanted_yaw = 0 # Vil ha samme rotasjon som den startet med
    wanted_yaw = np.rad2deg(wanted_yaw)%360
    yaw_cur = yaw_cur%360
    a=abs(shortestAngleFloat(yaw_cur, wanted_yaw))
    return -np.interp(a, [0, 180], [0, 1])+1  # type: ignore


def findGradient(x:float,y:float,a:float,b:float) -> float:
    """
    Finner gradienten til et punkt på en sirkel gitt et punkt og sirkel sentrum

    Parameters:
        x (float) Punkt i x retning  
        y (float) Punkt i y retning 
        a (float) Senter til sirkel i x retning 
        b (float) Senter til sirkel i y retning  

    Return: 
        fitness (np.float64) Hvor langt unna den var [0-1], større er bedre
    """
    gradient = -(x-a)/(y-b)
    return gradient

def findAngle(gradient:float)-> float:
    """
    Finner vinkelen i grader mellom  gradient og normalvektoren (0,1)

    Parameters:
        gradient (float) Punkt i x retning  

    Return: 
        angle_between_degree (float)
    """
    vector_start = 0
    vector_end = gradient
    vector = np.array([[0,vector_start], [1,vector_end]])
    vector_norm = vector/np.linalg.norm(vector)
    vector_up = np.array([[0,0],[0,1]])
    angle_between_r = np.arccos(np.clip(np.dot(vector_norm, vector_up), -10.0, 10.0))[1,1]
    angle_between_degree = np.rad2deg(angle_between_r)
    return angle_between_degree

def rotateAngle(angle_deg:float, x:float, y:float) -> float:
    """
    Roterer vinkelen basert på hvilken kvadrant den befinner seg i 

    Parameters:
        angle_deg (float) Hvor mange grader den er 
        x (float) Posisjon i x retning 
        y (float) Posisjon i y retning 
    Return: 
        vinkel (float)
    """
    if x>=0:
        if y>=0:
            return angle_deg
        else:
            return (angle_deg + 180)%360
    else:
        if y>=0:
            return (angle_deg + 180)%360
        else:
            return angle_deg

def findCircle(x1:float, y1:float, x2:float, y2:float, x3:float, y3:float) -> tuple[float, float, float]:
    """
    findCircle lager en sirkel basert på tre punkter

    Parameters:
        x1 (float) Punkt 1 i x retning 
        y1 (float) Punkt 1 i y retning
        x2 (float) Punkt 2 i x retning 
        y2 (float) Punkt 2 i y retning
        x3 (float) Punkt 3 i x retning 
        y4 (float) Punkt 3 i y retning

    Return: 
        sirkelsenter i x,y og radius tuple[float, float, float]
    """
    # Hentet fra: https://www.geeksforgeeks.org/equation-of-circle-when-three-points-on-the-circle-are-given/
    # Skrevet av: Ryuga
    x12 = x1 - x2; 
    x13 = x1 - x3; 

    y12 = y1 - y2; 
    y13 = y1 - y3; 

    y31 = y3 - y1; 
    y21 = y2 - y1; 

    x31 = x3 - x1; 
    x21 = x2 - x1; 
    # x1^2 - x3^2 
    sx13 = pow(x1, 2) - pow(x3, 2); 
    # y1^2 - y3^2 
    sy13 = pow(y1, 2) - pow(y3, 2); 

    sx21 = pow(x2, 2) - pow(x1, 2); 
    sy21 = pow(y2, 2) - pow(y1, 2); 

    f = (((sx13) * (x12) + (sy13) * (x12) + (sx21) * (x13) + (sy21) * (x13)) / (2 * ((y31) * (x12) - (y21) * (x13))));
             
    g = (((sx13) * (y12) + (sy13) * (y12) + (sx21) * (y13) + (sy21) * (y13)) / (2 * ((x31) * (y12) - (x21) * (y13)))); 
 
    c = (-pow(x1, 2) - pow(y1, 2) -
         2 * g * x1 - 2 * f * y1); 
 
    # eqn of circle be x^2 + y^2 + 2*g*x + 2*f*y + c = 0 
    # where centre is (h = -g, k = -f) and 
    # radius r as r^2 = h^2 + k^2 - c 
    h = -g; 
    k = -f; 
    sqr_of_r = h * h + k * k - c; 
 
    # r is the radius 
    r = round(np.sqrt(sqr_of_r), 5); 
    return h, k, r


def circleFitness(x_cur: float,y_cur: float,yaw_cur: float, count_collide:int=0) -> np.float64:
    """
    Fitnessfunksjon som finner ut hvor langt unna i vinkel den er i forhold til det den skulle ha hvert
    Basert på papers for å kunne oppfordre til rotasjon gitt en posisjon 

    Parameters:
        x_cur (float) Hvor langt i x retning den er 
        y_cur (float) Hvor langt i y retning den er
        yaw_cur (float) Hvor mye yaw den har vrid seg i grader
        count_collide (int) Antall ganger den har kollidert med bakken 

    Return: 
        fitness (np.float64) Hvor langt unna den var [0-1], større er bedre
    """
    x1 = 0 ; y1 = 0.01;
    x2 = 0 ; y2 = -0.01;
    # Ungår forskjellige edgecases 
    # For nærme 0,0:
    if np.sqrt(pow(x_cur, 2)+ pow(y_cur, 2)) < 1:
        angle_between_degree = 0
    # Hvis den ibare har gått rett frem 
    elif x_cur==0:
        if y_cur>= 0:
            angle_between_degree = 0
        else:
            angle_between_degree = 180
    # Hvis den har gått rett til siden 
    elif y_cur==0:
        angle_between_degree = 90
    # Alle andre muligheter 
    else:
        a,b,r = findCircle(x1, y1, x2, y2, x_cur, y_cur);
        gradient = findGradient(x_cur, y_cur, a,b)
        angle_between_degree = findAngle(gradient)
    wanted_yaw = rotateAngle(angle_between_degree, x_cur, y_cur)
    a=abs(shortestAngleFloat(yaw_cur, wanted_yaw))
    return -np.interp(a, [0, 180], [0, 1])+1 # type: ignore

 


if __name__ == "__main__":
    #circleFitness(3.5,2,3)
    print(circleFitness(0.001,0,0))
    #circleFitness(0.2,-4,40.1)
    #circleFitness(10,-6,6.8,0)