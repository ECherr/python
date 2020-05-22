import json

def read_result(filePath = "./result/result.txt"):
    with open(filePath, 'r') as f:
        dict = json.loads(f.read().strip())
        print('识别成功，内容为：' + dict['result'][0])
        music = str(dict['result'][0]).split('播放')[1]

def main():
    read_result()


if __name__ == '__main__':
    main()
