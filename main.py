from math import sqrt
import matplotlib.pyplot as plt

def Average(lst:list[float]) -> float:
    sum = 0
    for num in lst:
        sum += num
    return sum/len(lst)

def Distance(point1X:float, point2X:float, point1Y:float, point2Y:float) -> float:
    return sqrt((point1X-point2X)**2 + (point1Y-point2Y)**2)

def readPoints(fileName:str) -> tuple[list[float], list[float], int]:
    with open(fileName, 'r') as file:
        titles = file.readline()
        points = file.readlines()
        col1 = []
        col2 = []
        for point in points:
            val1, val2 = point.strip().split(',')
            col1.append(float(val1))
            col2.append(float(val2))

        pointCount = len(points)
            
        if titles[0] == 'Y':
            return col2, col1, pointCount
        else:
            return col1, col2, pointCount
        

def initCentroids(listofx:list[float], listofy:list[float], K:int) -> list[list[float]]:
    centroids = []
    for i in range(K):
        centroids.append([listofx[i], listofy[i]])
    return centroids

def initClusters(K:int) -> list[list[list[float]]]:
    clusters = []
    for _ in range(K):
        clusters.append([[], []])
    return clusters

def rebuildClusters(pointCount:int, Centroids:list[list[list[float]]], listofx:list[float], listofy:list[float], K:int) -> list[list[list[float]]]:
    clusters = initClusters(K)
    for i in range(pointCount):
        x = listofx[i]
        y = listofy[i]
        mn = 1e9
        idx = -1
        for j in range(len(Centroids)):
            centroid = Centroids[j]
            dist = Distance(centroid[0], x, centroid[1], y)
            if dist < mn:
                mn = dist
                idx = j
        clusters[idx][0].append(x)
        clusters[idx][1].append(y)
    return clusters

def reCalclculateCentroids(clusters:list[list[list[float]]], K:int) -> list[list[float]]:
    new_centroids = []
    for cluster in clusters:
        x_average = Average(cluster[0])
        y_average = Average(cluster[1])
        new_centroids.append([x_average, y_average])
    return new_centroids

def calculateLossValue(NewCentroids:list[list[float]], Centroids:list[list[float]], K:int) -> float:
    loss = 0
    for i in range(K):
        loss += Distance(NewCentroids[i][0], Centroids[i][0], NewCentroids[i][1], Centroids[i][1])
    return loss

def K_Means_iteration(pointCount:int, listofx:list[float], listofy:list[float], Centroids:list[list[float]], K:int) -> tuple[list[list[list[float]]], int, list[list[float]]]:
    clusters = rebuildClusters(pointCount, Centroids, listofx, listofy, K)
    new_centroids = reCalclculateCentroids(clusters, K)
    loss = calculateLossValue(new_centroids, Centroids, K)
    return clusters, loss, new_centroids
    

def showClusters(clusters:list[list[list[float]]], Xlabel:str, Ylabel:str, K:int,  Colors:list[str]) -> None:
    for i in range(K):
        cluster = clusters[i]
        plt.scatter(cluster[0], cluster[1], c=Colors[i])
    plt.show()

# Please do not change after this point

listofx, listofy, pointCount = readPoints("data.csv")
Xlabel = "X"
Ylabel = "Y"

plt.scatter(listofx, listofy)
plt.xlabel(Xlabel)
plt.ylabel(Ylabel)
plt.show()


totalIterations = 50
iterations = totalIterations
K = 6
Minimumloss = 0.0001

Centroids = initCentroids(listofx, listofy, K)
while iterations >= 0:
    clusters, loss, Centroids = K_Means_iteration(pointCount, listofx, listofy, Centroids, K)
    print("Epoch = %d"%(totalIterations - iterations + 1))
    print("Loss Function = %0.4f"%(loss))
    if(loss < Minimumloss):
        break
    iterations -= 1

Colors = ["red", "blue", "green", "black", "yellow", "purple", "magenta"]
showClusters(clusters, Xlabel, Ylabel, K, Colors)


