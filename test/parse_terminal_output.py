
prelude = "step_size = 0.02, momentum_eta = 0.9, regularization_lambda = 1e-06"

chi2 = []

def parse_line(line):
    l = line.split()
    print(l[3])
    return l[3]

with open("../core/GMRES_results.txt", "r") as f:
    lines = f.readlines()
    chi2_lines = []
    for line in lines:
        #chi square =  869.7910257577896
        if "chi square =" in line:
            chi2_lines.append(line)

    for line in chi2_lines:
        l = parse_line(line)
        chi2.append(l)

with open("test_xb.txt", "w") as f:
    f.write(prelude)
    f.write("\n")
    for i in chi2:
        f.write(i)
        f.write("  ")

f.close();
