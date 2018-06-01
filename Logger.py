
class Logger:
    def log(self, id, name, cost):
        file = open("log.txt", "a")
        file.write(
            "Sell id {0}. Product Name {1}. Cost {2}\n".format(id, name, cost))
        file.close()


logger = Logger()
logger.log(3, "Tea", 12)
logger.log(4, "Water", 9)
