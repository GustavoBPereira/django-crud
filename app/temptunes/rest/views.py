from rest_framework import permissions, views, status
from rest_framework.response import Response

from app.temptunes.rest.serializers import ClimatePlaylistSerializer
from app.temptunes.usecases import PlayListByCityUseCase
from app.temptunes.usecases.exceptions import (
    CityNotFound,
    PlaylistNotFound,
    UnknownPartnerError,
)


class CitySongSuggestionView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, city: str):
        usecase = PlayListByCityUseCase()
        try:
            data = usecase.run(city)
        except CityNotFound:
            return Response(
                {"reason": "city not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except PlaylistNotFound:
            return Response(
                {"reason": "playlist not found"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except UnknownPartnerError:
            return Response(
                {"reason": "Unknown error from partner"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"reason": f"Unknown error from server {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        serializer = ClimatePlaylistSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
