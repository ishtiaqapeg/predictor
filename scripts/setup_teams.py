#!/usr/bin/env python3
"""
Скрипт для настройки словаря команд
Создает пример Google Sheet с командами NCAA D1
"""
import csv
import io

def create_teams_csv():
    """Создает CSV файл с командами NCAA D1"""
    
    # Пример команд NCAA D1 (основные)
    teams = [
        # ACC
        ("duke", "Duke"),
        ("north carolina", "North Carolina"),
        ("virginia", "Virginia"),
        ("florida state", "Florida State"),
        ("louisville", "Louisville"),
        ("syracuse", "Syracuse"),
        ("miami", "Miami"),
        ("clemson", "Clemson"),
        ("north carolina state", "NC State"),
        ("boston college", "Boston College"),
        ("pittsburgh", "Pittsburgh"),
        ("georgia tech", "Georgia Tech"),
        ("wake forest", "Wake Forest"),
        ("notre dame", "Notre Dame"),
        ("virginia tech", "Virginia Tech"),
        
        # Big Ten
        ("michigan state", "Michigan State"),
        ("michigan", "Michigan"),
        ("ohio state", "Ohio State"),
        ("purdue", "Purdue"),
        ("wisconsin", "Wisconsin"),
        ("illinois", "Illinois"),
        ("iowa", "Iowa"),
        ("maryland", "Maryland"),
        ("rutgers", "Rutgers"),
        ("penn state", "Penn State"),
        ("northwestern", "Northwestern"),
        ("indiana", "Indiana"),
        ("minnesota", "Minnesota"),
        ("nebraska", "Nebraska"),
        
        # Big 12
        ("kansas", "Kansas"),
        ("baylor", "Baylor"),
        ("texas", "Texas"),
        ("texas tech", "Texas Tech"),
        ("oklahoma", "Oklahoma"),
        ("oklahoma state", "Oklahoma State"),
        ("iowa state", "Iowa State"),
        ("kansas state", "Kansas State"),
        ("west virginia", "West Virginia"),
        ("tcu", "TCU"),
        
        # SEC
        ("kentucky", "Kentucky"),
        ("tennessee", "Tennessee"),
        ("auburn", "Auburn"),
        ("alabama", "Alabama"),
        ("arkansas", "Arkansas"),
        ("florida", "Florida"),
        ("georgia", "Georgia"),
        ("louisiana state", "LSU"),
        ("mississippi", "Ole Miss"),
        ("mississippi state", "Mississippi State"),
        ("missouri", "Missouri"),
        ("south carolina", "South Carolina"),
        ("texas a&m", "Texas A&M"),
        ("vanderbilt", "Vanderbilt"),
        
        # Pac-12
        ("arizona", "Arizona"),
        ("ucla", "UCLA"),
        ("oregon", "Oregon"),
        ("usc", "USC"),
        ("stanford", "Stanford"),
        ("california", "California"),
        ("washington", "Washington"),
        ("washington state", "Washington State"),
        ("oregon state", "Oregon State"),
        ("arizona state", "Arizona State"),
        ("utah", "Utah"),
        ("colorado", "Colorado"),
        
        # Big East
        ("villanova", "Villanova"),
        ("connecticut", "UConn"),
        ("creighton", "Creighton"),
        ("xavier", "Xavier"),
        ("providence", "Providence"),
        ("seton hall", "Seton Hall"),
        ("st. johns", "St. John's"),
        ("butler", "Butler"),
        ("depaul", "DePaul"),
        ("georgetown", "Georgetown"),
        ("marquette", "Marquette"),
        
        # Atlantic 10
        ("dayton", "Dayton"),
        ("richmond", "Richmond"),
        ("saint louis", "Saint Louis"),
        ("davidson", "Davidson"),
        ("st. bonaventure", "St. Bonaventure"),
        ("rhode island", "Rhode Island"),
        ("massachusetts", "UMass"),
        ("george mason", "George Mason"),
        ("la salle", "La Salle"),
        ("saint josephs", "Saint Joseph's"),
        ("duquesne", "Duquesne"),
        ("fordham", "Fordham"),
        ("george washington", "George Washington"),
        ("st. bonaventure", "St. Bonaventure"),
        
        # Mountain West
        ("san diego state", "San Diego State"),
        ("nevada", "Nevada"),
        ("utah state", "Utah State"),
        ("boise state", "Boise State"),
        ("new mexico", "New Mexico"),
        ("colorado state", "Colorado State"),
        ("fresno state", "Fresno State"),
        ("wyoming", "Wyoming"),
        ("air force", "Air Force"),
        ("san jose state", "San Jose State"),
        ("unlv", "UNLV"),
        
        # American Athletic
        ("houston", "Houston"),
        ("memphis", "Memphis"),
        ("cincinnati", "Cincinnati"),
        ("wichita state", "Wichita State"),
        ("temple", "Temple"),
        ("south florida", "South Florida"),
        ("tulane", "Tulane"),
        ("tulsa", "Tulsa"),
        ("east carolina", "East Carolina"),
        ("southern methodist", "SMU"),
        ("central florida", "UCF"),
        
        # West Coast
        ("gonzaga", "Gonzaga"),
        ("saint marys", "Saint Mary's"),
        ("byu", "BYU"),
        ("san francisco", "San Francisco"),
        ("santa clara", "Santa Clara"),
        ("pepperdine", "Pepperdine"),
        ("loyola marymount", "Loyola Marymount"),
        ("san diego", "San Diego"),
        ("portland", "Portland"),
        ("pacific", "Pacific"),
    ]
    
    # Создаем CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Заголовки
    writer.writerow(["alias", "canonical"])
    
    # Записываем команды
    for alias, canonical in teams:
        writer.writerow([alias, canonical])
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content

def main():
    """Основная функция"""
    print("Creating NCAA D1 teams CSV...")
    
    csv_content = create_teams_csv()
    
    # Сохраняем в файл
    with open("teams.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    print(f"Created teams.csv with {len(csv_content.splitlines())-1} teams")
    print("\nTo use this file:")
    print("1. Upload to Google Sheets")
    print("2. Make it publicly accessible")
    print("3. Get the CSV export URL")
    print("4. Set TEAMLIST_CSV_URL in your .env file")

if __name__ == "__main__":
    main()
