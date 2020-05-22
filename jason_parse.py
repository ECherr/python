import json

def read_result(filePath = "./result/result.txt"):
    with open(filePath, 'r') as f:
        dict = f.read().strip()
        return dict

def main():
    dict = json.loads(read_result())
    print(dict['result'][0])


if __name__ == '__main__':
    main()
