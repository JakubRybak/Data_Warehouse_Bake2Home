import subprocess
import csv

def main():
    print("Eksportowanie współrzędnych klientów z bazy do pliku customers.csv...")
    # Twardo ciągniemy ID by wiedzieć ilu ich dokładnie jest w CSV
    cmd = 'docker exec -i postgres_db psql -U admin -d customer-manager-db -t -A -c "SELECT \\"CustomerId\\", \\"Latitude\\", \\"Longitude\\" FROM \\"CustomerAddress\\" WHERE \\"Latitude\\" > 0 AND \\"Longitude\\" > 0;"'
    
    try:
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
        lines = [line.strip() for line in output.split('\n') if line.strip()]
        
        with open('customers.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['CustomerId', 'Latitude', 'Longitude'])
            
            for line in lines:
                parts = line.split('|')
                if len(parts) == 3:
                    writer.writerow([parts[0], parts[1], parts[2]])
                    
        print(f"Sukces! Ściągnięto {len(lines)} punktów do pliku customers.csv")
    except Exception as e:
        print(f"Błąd przy eksporcie: {e}")

if __name__ == '__main__':
    main()
