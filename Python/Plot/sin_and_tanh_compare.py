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

    fig, ax = plt.subplots(figsize=(5.5, 4))

    ax.plot(t, sin, label="A∗sin(2π ∗t∗f +ϕ)+θ")
    ax.plot(t, tanh, label="A∗tanh(4∗sin(2π ∗(t ∗f +ϕ))+θ")
    ax.set_title("Sammenligning mellom kontrollfunksjoner")
    ax.legend(loc='upper left',fontsize=8)
    ax.set_xlabel("Tid", fontdict=dict(fontsize=12))
    ax.set_ylabel("Verdi", fontdict=dict(fontsize=12))
    plt.grid()
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    show()