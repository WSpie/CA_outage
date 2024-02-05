Target [CA outage map](https://pgealerts.alerts.pge.com/outage-tools/outage-map/#)
It's hard to scrape direcly, we use alternative approach here.

# Run
```
python main.py --n-cpus 20 (default 1)
```
# Outputs
The csv will named by the time you run the code.

Preview of outputs\02_04_2024_21.43.csv:
| outage_type | city          | outage_cause | count | county        | version             | display       | level  |
|-------------|---------------|--------------|-------|---------------|---------------------|---------------|--------|
| CURRENT     | san jose      | STORM        | 69055 | santa clara   | 2024-02-04 19:27:23 | santa clara   | county |
| CURRENT     | stockton      | STORM        | 27843 | san joaquin   | 2024-02-04 19:27:23 | stockton      | city   |
| CURRENT     | san francisco | STORM        | 24366 | san francisco | 2024-02-04 19:27:23 | san francisco | county |
| CURRENT     | daly city     | STORM        | 7741  | san mateo     | 2024-02-04 19:27:23 | daly city     | city   |
| CURRENT     | sunnyvale     | STORM        | 7553  | santa clara   | 2024-02-04 19:27:23 | santa clara   | county |

# Schedule and run
Use cron to set scheduled commands [file](schedule_n_run.sh):

## 1. Configurate .sh
In scheduled commands, make sure use absolute path anywhere.

## 2. Schedule
Ensure script is executable
```
chmod +x /path/to/your/script.sh
```
Open crontable file
```
crontab -e
```
Add a cron job
```
# MIN HOUR DOM MON DOW COMMAND
0 */3 * * * /path/to/schedule_n_run.sh >> /path/to/logfile 2>&1
# e.g. run code every 3 hours
```
Check log at /path/to/logfile