from flask_restful import Resource, reqparse
from models.hotel import HotelModel


hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.5,
        'diaria': 480.85,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.5,
        'diaria': 250.00,
        'cidade': 'São Paulo'
    },
    {
        'hotel_id': 'delta',
        'nome': 'Delta Hotel',
        'estrelas': 3.0,
        'diaria': 220.50,
        'cidade': 'Belo Horizonte'
    },
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        hoteis.append(hotel.json())

        return hotel.json(), 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        hoteis.append(hotel.json())

        if Hotel.find_hotel(hotel_id):
            Hotel.find_hotel(hotel_id).update(hotel.json())
            return hotel.json(), 200

        hoteis.append(hotel.json())
        return hotel.json(), 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}
