import json

vnstat_file = open('vnstat.txt')
vnstat_json = json.load(vnstat_file)
vnstat_file.close()

print(f"{int(vnstat_json['interfaces'][0]['traffic']['hour'][-1]['tx']) / 2 ** 30:.1f}")
