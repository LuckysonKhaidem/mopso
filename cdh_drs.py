from pyswarm import pso
from penalties import l1_equality_penalty as equality_penalty, l1_inequality_penalty as inequality_penalty
import pandas as pd



def interior_score(radius, density, alpha, beta):
    return (radius**alpha) * (density**beta)

def surface_score(escape_velocity, surface_temperature, gamma, delta):
    return (escape_velocity**gamma) * (surface_temperature**delta)



def optimize(radius, density, escape_velocity, surface_temperature):
    tolerance = 10e-7
    error = 10e-6

    def f1(x):
        score = interior_score(radius, density,x[0],x[1])
        objective = -score + inequality_penalty((x[0] + x[1]) - 1, error) +inequality_penalty(-x[0],error) + inequality_penalty(x[0]-1,error)+inequality_penalty(-x[1],error)+inequality_penalty(x[1]-1,error)
        return objective

    def f2(x):
        score = surface_score(escape_velocity, surface_temperature,x[0],x[1])
        objective = -score + inequality_penalty((x[0] + x[1]) -1, error) +inequality_penalty(-x[0],error) + inequality_penalty(x[0]-1,error)+inequality_penalty(-x[1],error)+inequality_penalty(x[1]-1,error)
        return objective
   

    interior_soln,int_score = pso(
           f1, 
           lb = [-20,-20], ub = [20,20], 
           swarmsize = 300, 
           omega = 0.05,phip = 0.01, phig = 0.85,
           maxiter = 300, minfunc = 10e-20,
           minstep = 10e-20
     )

    surface_soln,surf_score = pso(f2, lb = [-20,-20], ub = [20,20],
                         swarmsize = 300,
                         omega = 0.05, phip = 0.01, phig = 0.85,
                         maxiter = 300, minfunc= 10e-20,
                         minstep = 10e-20,
                        )
    
    return interior_soln, surface_soln, int_score, surf_score


if __name__ == "__main__":
    p_names = [ "GJ 176 b",
                "GJ 667 C b",
                "GJ 667 C e",
                "GJ 667 C f",
                "GJ 3634 b",
                "HD 40307 e",
                "HD 40307 f",
                "HD 40307 g",
                "Kepler-186 f",
                "Proxima Cen b",
                "TRAPPIST-1 b", 
                "TRAPPIST-1 c", 
                "TRAPPIST-1 d",
                "TRAPPIST-1 e",
                "TRAPPIST-1 g"]
    alphas = []
    betas = []
    gammas = []
    deltas = []
    surface_scores = []
    interior_scores = []
    df = pd.read_csv("phl_hec_all_confirmed 2.csv")
    df = df[df["P. Name"].isin(p_names)]
    radii = df["P. Radius (EU)"].tolist()
    densities = df["P. Density (EU)"].tolist()
    esc_velocities = df["P. Esc Vel (EU)"].tolist()
    surf_temps = (df["P. Ts Mean (K)"]/ 288.0).tolist()

    print len(radii),len(densities), len(esc_velocities), len(surf_temps), len(p_names)
    for i in xrange(len(p_names)):
        print "optimizing for {}".format(p_names[i])
        interior_soln, surface_soln,int_score, surf_score = optimize(radii[i], densities[i], esc_velocities[i], surf_temps[i])
        alphas.append(interior_soln[0])
        betas.append(interior_soln[1])

        gammas.append(surface_soln[0])
        deltas.append(surface_soln[1])

        surface_scores.append(-surf_score)
        interior_scores.append(-int_score)

    output = pd.DataFrame({"p_names" : p_names, 
                           "alphas" : alphas, 
                           "betas" : betas, 
                          "interior scores" : interior_scores, 
                          "gammas" : gammas, 
                          "deltas" : deltas, 
                          "surface scores" : surface_scores})
   
    output = output[["p_names", "alphas", "betas", "interior scores", "gammas", "deltas", "surface scores"]]
    output.to_csv("out_drs.csv", index = False)


