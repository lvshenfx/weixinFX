import requests
from flask import Flask, jsonify, send_file, request
import matplotlib.pyplot as plt
import io
import pytz  
from datetime import datetime

app = Flask(__name__)

@app.route('/get_line_chart', methods=['GET'])
def get_line_chart():
    # 发起API请求以获取数据
    #url = "https://yuce.vercel.app/get_code_date"
    url = "https://helloyuce.yixinfx.asia/get_code_date"  
    symbol = request.args.get('symbol')

    params = {'symbol': symbol}
    china_tz = pytz.timezone('Asia/Shanghai')  
    now_bj = datetime.now(china_tz)  
    yuce_date_str = now_bj.date()  
    yuce_date = yuce_date_str.strftime('%Y.%m.%d')
    response = requests.get(url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析JSON响应
        data = response.json()

        # 从响应中提取日期和价格列表
        dates = data.get('shijian', [])
        prices = data.get('kongjian', [])
        # 清除当前图像
        plt.clf()
        # 绘制折线图
        plt.plot(dates, prices)
        #plt.xlabel('Dates')
        #plt.ylabel('Prices')
        plt.title(symbol+"---"+yuce_date)
        # 旋转x轴标签，使其竖直显示  
        plt.xticks(rotation=90)  
        # 设置刻度字体大小
        plt.xticks(fontsize=5)
        # 将图像保存到内存中的字节缓冲区
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        # 将图像作为响应发送
        return send_file(buf, mimetype='image/png')
    else:
        return jsonify({"error": "无法从API获取数据"})
# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])
