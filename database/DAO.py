from database.DB_connect import DBConnect
from model.Artist import Artist


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "select distinct g.Name from genre g "

        cursor.execute(query)

        for row in cursor:
            results.append(row["Name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genere):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select ar.ArtistId, ar.Name 
                    from artist ar, album al, track t, genre g
                    where ar.ArtistId = al.ArtistId 
                    and al.AlbumId = t.AlbumId 
                    and g.GenreId = t.GenreId 
                    and g.Name = %s
                    group by ar.ArtistId, ar.Name"""

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append(Artist(row["ArtistId"], row["Name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie(genere, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []

        query = """select ar1.ArtistId as id1, ar2.ArtistId as id2
                    from artist ar1,  artist ar2, album al1, album al2, track t1, track t2, genre g,
                    invoiceLine il1, Invoice i1, invoiceLine il2, Invoice i2, customer c 
                    where c.CustomerId = i1.CustomerId 
                    and i1.InvoiceId = il1.InvoiceId 
                    and il1.TrackId = t1.TrackId 
                    and t1.AlbumId = al1.AlbumId 
                    and al1.ArtistId = ar1.ArtistId 
                    and t1.GenreId = g.GenreId 
                    and c.CustomerId = i2.CustomerId 
                    and i2.InvoiceId = il2.InvoiceId 
                    and il2.TrackId = t2.TrackId 
                    and t2.AlbumId = al2.AlbumId 
                    and al2.ArtistId = ar2.ArtistId 
                    and t2.GenreId = g.GenreId  
                    and g.Name = %s
                    and ar1.ArtistId < ar2.ArtistId 
                    group by ar1.ArtistId, ar2.ArtistId"""

        cursor.execute(query, (genere,))

        for row in cursor:
            n1 = idMap[row["id1"]]
            n2 = idMap[row["id2"]]
            results.append((n1, n2))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarita():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        results = []

        query = """SELECT ar.ArtistId as id, COUNT(*) as popolarita
                    FROM artist ar, album al, track t, invoiceline il, invoice i
                    WHERE ar.ArtistId = al.ArtistId
                    and al.AlbumId = t.AlbumId
                    and t.TrackId = il.TrackId
                    and il.InvoiceId = i.InvoiceId
                    GROUP BY ar.ArtistId"""

        cursor.execute(query, )

        for row in cursor:
            results.append((row["id"], row["popolarita"]))

        cursor.close()
        conn.close()
        return results
