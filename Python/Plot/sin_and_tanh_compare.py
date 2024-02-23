import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

def show():
    A=1
    F=1
    PHI=0
    THETA=0
    t = np.arange(0, 2.01, 0.01)
    sin = A*np.sin(2*np.pi*t*F + PHI) + THETA
    tanh = A*np.tanh(4*np.sin(2*np.pi*(t*F+PHI))) + THETA

    plt.plot(t, sin, label="Sinus")
    plt.plot(t, tanh, label="Tanh")
    plt.title("Sammenligning mellom kontrollfunksjoner")
    plt.xlabel("Tid")
    plt.ylabel("Verdi")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    show()