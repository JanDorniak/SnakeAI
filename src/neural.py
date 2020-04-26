import numpy as np


def sigmoid(X):
    return 1/(1+np.exp(-X))


def ReLU(x):
    return x * (x > 0)


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)


class NeuralNetwork:

    # neuroN - array with n of neurons in each layer (at least 2 layers: in, out)
    def __init__(self, neuronN, network=None):
        if network == None:
            self.layersN = len(neuronN)
            self.weighs = []
            self.biases = []

            for i in range(1, self.layersN):
                self.weighs.append(np.random.rand(neuronN[i-1], neuronN[i]))
                self.biases.append(2 * np.random.rand(neuronN[i]) - 1)
        else:
            self.layersN = network.layersN
            self.weighs = []
            self.biases = []
            for weigh in network.weighs:
                self.weighs.append(weigh.copy())
            for bias in network.biases:
                self.biases.append(bias.copy())

    def predict(self, input):
        output = np.matmul(input, self.weighs[0])
        output = np.add(output, self.biases[0])
        output = list(map(ReLU, output))

        for i in range(1, self.layersN - 1):
            output = np.matmul(output, self.weighs[i])
            output = np.add(output, self.biases[i])
            if (i != self.layersN - 2):
                output = list(map(ReLU, output))

        return softmax(output)

    def mutate(self, chance):
        for w in self.weighs:
            for x in w:
                if np.random.rand() < chance:
                    randomNumber = np.random.normal(0, 0.1)
                    x += randomNumber

        for b in self.biases:
            for x in b:
                if np.random.rand() < chance:
                    randomNumber = np.random.normal(0, 0.1)
                    b += randomNumber

    def combine(self, other):
        for i in range(0, len(self.weighs)):
            w = self.weighs[i]
            otherw = other.weighs[i]
            partition1 = np.random.randint(0, np.size(w, 0))
            partition2 = np.random.randint(0, np.size(w, 1))
            for i in range(partition1, np.size(w, 0)):
                for j in range(partition2, np.size(w, 1)):
                    w[i][j] = otherw[i][j]

        for i in range(0, len(self.biases)):
            b = self.biases[i]
            otherb = other.biases[i]
            partition1 = np.random.randint(0, np.size(b, 0))
            for i in range(partition1, np.size(b, 0)):
                b[i] = otherb[i]

    def saveWeighs(self, number):
        for i in range(0, self.layersN - 1):
            np.savetxt('models/weighs' + str(i) + str(number) + '.csv',
                       self.weighs[i], delimiter=',')
            np.savetxt('models/biases' + str(i) + str(number) + '.csv',
                       self.biases[i], delimiter=',')

    def readWeighs(self, number):
        self.weighs = []
        self.biases = []
        for i in range(0, self.layersN - 1):
            self.weighs.append(np.loadtxt(
                'models/weighs' + str(i) + str(number) + '.csv', delimiter=','))
            self.biases.append(np.loadtxt(
                'models/biases' + str(i) + str(number) + '.csv', delimiter=','))
