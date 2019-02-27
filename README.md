# mrt-interesting-asns
python3 code to watch a directory of mrt files for activity from interesting ASNs

## installation

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### other requirements

*   [Isolario Project bgpscanner](https://isolario.it/web_content/php/site_content/tools.php)

## usage

```
echo "ASN|description" >> aslist.txt
watchmedo shell-command \
  --recursive --ignore-directories \
  --command='if [ "${watch_event_type}" = "modified" ]; then date; bgpscanner "${watch_src_path}" | /path/to/mrt-interesting-asns/mrt-interesting-asns.py; fi' \
  /home/mrt
```
