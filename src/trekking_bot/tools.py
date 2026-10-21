class TourInfoTool:
    def __init__(self):
        
        self.tours = {
            "sentiero_degli_dei": {
                "name": "Sentiero degli Dei",
                "description": "Percorso panoramico sulla Costiera Amalfitana",
                "duration": "5 ore",
                "difficulty": "media",
                "price": 45.00,
            },
            "gran_sasso": {
                "name": "Gran Sasso",
                "description": "Salita al Corno Grande con guida alpina",
                "duration": "8 ore",
                "difficulty": "alta",
                "price": 80.00,
            },
            "cinque_terre": {
                "name": "Cinque Terre",
                "description": "Traversata dei borghi lungo il sentiero azzurro",
                "duration": "6 ore",
                "difficulty": "facile",
                "price": 55.00,
            },
            "monte_cimone": {
                "name": "Monte Cimone",
                "description": "Anello sul crinale dell'Appennino settentrionale",
                "duration": "7 ore",
                "difficulty": "media",
                "price": 60.00,
            },
        }

    def get_info(self, tour_name: str) -> str:
        # 1. Normalizza il nome ricevuto 
        key = tour_name.lower().replace(" ", "_")

        tour = self.tours.get(key)

        if not tour:
            return f"Escursione non trovata. Ecco quelle disponibili: {self.tours}"

        return (
            f"Escursione: {tour['name']}\n"
            f"Descrizione: {tour['description']}\n"
            f"Durata: {tour['duration']}\n"
            f"Difficoltà: {tour['difficulty']}\n"
            f"Prezzo: €{tour['price']}"
        )

class DepartureTool:
    def __init__(self):
    
        self.departures = {
            "sentiero_degli_dei": [
                {"date": "2027-03-14", "time": "08:00", "seats": 6},
                {"date": "2027-03-28", "time": "08:00", "seats": 0},
                {"date": "2027-04-11", "time": "08:00", "seats": 10},
            ],
            "gran_sasso": [
                {"date": "2027-06-06", "time": "05:30", "seats": 4},
                {"date": "2027-06-20", "time": "05:30", "seats": 8},
            ],
            "cinque_terre": [
                {"date": "2027-04-03", "time": "09:00", "seats": 12},
                {"date": "2027-04-17", "time": "09:00", "seats": 3},
            ],
            "monte_cimone": [
                {"date": "2027-05-09", "time": "07:30", "seats": 7},
            ],
        }

    def get_departures(self, tour_name: str) -> str:
        key = tour_name.lower().replace(" ", "_")
        trips = self.departures.get(key)

        if trips is None:
            return f"Escursione non trovata. Disponibili: {list(self.departures)}"

        # tieni partenze con posti liberi
        available = [t for t in trips if t["seats"] > 0]

        if not available:
            return "Nessuna partenza con posti liberi per questa escursione."

        lines = [
            f"- {t['date']} alle {t['time']} ({t['seats']} posti liberi)"
            for t in available
        ]
        return "Prossime partenze:\n" + "\n".join(lines)

class GuideBookingTool:
    def __init__(self):
        # accumulo prenotazioni
        self.bookings = []

    def book_guide(self, tour_name: str, date: str, customer_name: str) -> str:
        booking = {
            "id": len(self.bookings) + 1,
            "tour": tour_name,
            "date": date,
            "customer": customer_name,
        }
        self.bookings.append(booking)

        return (
            f"Prenotazione confermata! Codice: {booking['id']}\n"
            f"Escursione: {tour_name}\n"
            f"Data: {date}\n"
            f"Intestata a: {customer_name}"
        )

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_tour_info",
            "description": "Restituisce i dettagli di un'escursione: descrizione, durata, difficoltà e prezzo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tour_name": {
                        "type": "string",
                        "description": "Nome dell'escursione, ad esempio 'Gran Sasso'.",
                    }
                },
                "required": ["tour_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_departures",
            "description": "Restituisce le prossime partenze con posti liberi di un'escursione.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tour_name": {
                        "type": "string",
                        "description": "Nome dell'escursione, ad esempio 'Cinque Terre'.",
                    }
                },
                "required": ["tour_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "book_guide",
            "description": (
                "Prenota una guida per un'escursione. Chiamala solo dopo aver "
                "chiesto all'utente escursione, data e nome: non inventare i valori."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tour_name": {
                        "type": "string",
                        "description": "Nome dell'escursione da prenotare.",
                    },
                    "date": {
                        "type": "string",
                        "description": "Data della partenza, formato AAAA-MM-GG.",
                    },
                    "customer_name": {
                        "type": "string",
                        "description": "Nome e cognome di chi prenota.",
                    },
                },
                "required": ["tour_name", "date", "customer_name"],
            },
        },
    },
]


tour_info = TourInfoTool()
departures = DepartureTool()
booking = GuideBookingTool()

AVAILABLE_FUNCTIONS = {
    "get_tour_info": tour_info.get_info,
    "get_departures": departures.get_departures,
    "book_guide": booking.book_guide,
}


def run_tool(name: str, arguments: dict) -> str:
    function = AVAILABLE_FUNCTIONS.get(name)

    if function is None:
        return f"Tool sconosciuto: {name}"

    try:
        return function(**arguments)
    except TypeError:
        return f"Argomenti non validi per {name}: {arguments}"