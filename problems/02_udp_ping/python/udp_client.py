import logging
import socket
import time

logging.basicConfig(level=logging.INFO)

host = '127.0.0.1'
port = 12345
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 设置套接字超时值为1秒
client.settimeout(1)
send_times = 10
min_rtt, max_rtt, total_rtt, lost_times = float('inf'), float('-inf'), 0, 0
for i in range(1, send_times + 1):
    t = time.time()
    message = f'Ping {i} {t}'
    client.sendto(message.encode('utf-8'), (host, port))
    try:
        response, _ = client.recvfrom(1024)
        rtt = time.time() - t
        # 计算最小RTT、最大RTT、RTT总和
        min_rtt = min(min_rtt, rtt)
        max_rtt = max(max_rtt, rtt)
        total_rtt += rtt
        logging.info(f'Reply is `{response.decode("utf-8")}`')
        logging.info(f"Sequence {i}'s RTT is {rtt:3f}")
    except socket.timeout:
        lost_times += 1
        logging.warning(f'Sequence {i} is lost')

lost_rate = lost_times / send_times
logging.info(f'Lost rate in percentage is {lost_rate * 100}%')
if lost_rate != 1:
    logging.info(
        f'Minimum RTT is {min_rtt:3f}, '
        f'maximum RTT is {max_rtt:3f}, '
        f'average RTT is {total_rtt / (send_times - lost_times):3f}'
    )
