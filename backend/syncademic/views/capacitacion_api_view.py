from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import permissions

from ..models.capacitacion import Capacitacion
from ..serializers import ListaDocenteSerializer
from ..serializers import ListaAsignaturasSerializer
from ..serializers import ListaCapacitacionSerializer, CapacitacionSerializer
from ..services import CapacitacionService
from ..exceptions.not_found import ObjectNotFound


class CapacitacionAPIView(viewsets.ModelViewSet):
    queryset = Capacitacion.objects.all()
    serializer_class_Docente = ListaDocenteSerializer
    serializer_class_Asignatura = ListaAsignaturasSerializer
    permission_classes = (permissions.AllowAny,)
    service = CapacitacionService()

    #get lista de capacitaciones de un profesor
    @action(detail=False, methods=['get'],
            url_path='(?P<id_docente>[^/.]+)/capacitaciones')
    def get_promedios(self, request, id_docente):
        self.service.id_docente = id_docente

        try:
            docente = self.service.get_lista_capacitaciones(id_docente)
            return Response(docente, status=status.HTTP_200_OK)
        except ObjectNotFound as e:
            return Response({'Error': e.detail}, status=status.HTTP_404_NOT_FOUND)

    #get lista docentes
    @action(detail=False, methods=['get'], url_path='docentes')
    def get(self, request):

        try:
            docentes = self.service.get_lista_docentes()
            serializer = ListaDocenteSerializer(docentes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectNotFound as e:
            return Response({'Error': e.detail}, status=status.HTTP_404_NOT_FOUND)

    #get lista capacitaciones
    @action(detail=False, methods=['get'], url_path='capacitaciones')
    def get(self, request):

        try:
            capacitaciones = self.service.get_lista_docentes()
            serializer = ListaCapacitacionSerializer(capacitaciones, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectNotFound as e:
            return Response({'Error': e.detail}, status=status.HTTP_404_NOT_FOUND)

    #get lista de capacitaciones de un docente
    @action(detail=False, methods=['get'], url_path='(?P<id_docente>[^/.]+)/capacitaciones')
    def get(self, request, id_profesor):

        try:
            capacitaciones = self.service.get_docente(id_profesor)
            serializer = ListaCapacitacionSerializer(capacitaciones, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectNotFound as e:
            return Response({'Error': e.detail}, status=status.HTTP_404_NOT_FOUND)

    # get lista de puntuaciones de un docente
    @action(detail=False, methods=['get'], url_path='(?P<id_docente>[^/.]+)/puntuacionesViejas')
    def get(self, request, id_docente):

            try:
                puntuaciones = self.service.get_lista_puntuaciones(id_docente)
                serializer = ListaCapacitacionSerializer(puntuaciones, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectNotFound as e:
                return Response({'Error': e.detail}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'], url_path='(?P<id_profesor>[^/.]+)/(?P<periodo>[^/.]+)/nuevo')
    def post(self, request, id_profesor, periodo):

        for capacitacion_data in request.data:
            data = {
                'id_profesor': capacitacion_data['id_profesor'],
                'nombre': capacitacion_data['nombre'],
                'area': capacitacion_data['area'],
                'periodo': capacitacion_data['periodo']
            }

            self.service.id_profesor = id_profesor
            self.service.periodo = periodo

            self.service.save_capacitacion(data)

        mensaje = self.service.get_alertas()

        return Response(mensaje, status=status.HTTP_201_CREATED)
