#
# Complete the 'processLogs' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. STRING_ARRAY logs
#  2. INTEGER threshold
#

def processLogs(logs, threshold):
    # Write your code here
    counter_dic = {}
    over_threshold = []
    for log in logs:
        send_id, recip_id, amount =  log.split()
        unique_ids = [send_id, recip_id]
        for user in unique_ids:
            try:
                counter_dic[user] += 1
            except KeyError:
                counter_dic[user] = 1
    for k, v in counter_dic.items():
        if v >= threshold:
            over_threshold.append(k)
    if len(over_threshold) == 0:
        over_threshold.append("0")
    over_threshold.sort(key=int)
    return over_threshold