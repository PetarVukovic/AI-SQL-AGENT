def get_examples():
    examples = [
    
    {
        "input":'',
        'query':'',
    },
    {   "input": "List all artists.",
        "query": "SELECT * FROM Artist;"
    },
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
    
    {
        "input": "List all employees ",
        "query": 'SELECT * FROM "Employee"',
    },
    
    {
        "input": "List all from Reactivities.",
        'query':'SELECT COUNT(*) FROM [Reactivities].[dbo].[Activities]',
    },
    {
        "input":'Daj mi prvih 10  vrijednosti iz Bidova',
        "query":""" select top 10 RegulationUnitEic
            FROM [AdnetBalancingMarket_Local].[Bid].[EnergyBids]
            where ProductTypeId in (4,5) and StatusId in (2,6) 
            GROUP BY RegulationUnitEic,TimeFrom,ProductTypeId
            order by TimeFrom""",
    }
    
    
    ]
    return examples    

