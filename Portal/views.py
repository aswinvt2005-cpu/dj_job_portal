from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Application


class JobManager(APIView):

    def post(self, request):

        data = request.data

        job = Job.objects.create(
            title=data.get('title'),
            company=data.get('company'),
            location=data.get('location'),
            salary=data.get('salary'),
            description=data.get('description'),
            requirements=data.get('requirements')
        )

        return Response({
            'message': 'Job added successfully',
            'job_id': job.id
        }, status=status.HTTP_201_CREATED)

    def get(self, request):

        jobs = Job.objects.all()

        data = []

        for job in jobs:
            data.append({
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'salary': job.salary,
                'description': job.description,
                'requirements': job.requirements
            })

        return Response(data)


class JobDetails(APIView):

    def get(self, request, id):

        try:
            job = Job.objects.get(id=id)

            data = {
                'id': job.id,
                'title': job.title,
                'company': job.company,
                'location': job.location,
                'salary': job.salary,
                'description': job.description,
                'requirements': job.requirements
            }

            return Response(data)

        except Job.DoesNotExist:
            return Response(
                {'message': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, id):

        try:
            job = Job.objects.get(id=id)

            job.title = request.data.get('title', job.title)
            job.company = request.data.get('company', job.company)
            job.location = request.data.get('location', job.location)
            job.salary = request.data.get('salary', job.salary)
            job.description = request.data.get('description', job.description)
            job.requirements = request.data.get('requirements', job.requirements)

            job.save()

            return Response({'message': 'Job updated successfully'})

        except Job.DoesNotExist:
            return Response(
                {'message': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, id):

        try:
            job = Job.objects.get(id=id)
            job.delete()

            return Response({'message': 'Job deleted successfully'})

        except Job.DoesNotExist:
            return Response(
                {'message': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ApplicationManager(APIView):

    def post(self, request):

        data = request.data

        try:
            job = Job.objects.get(id=data.get('job_id'))

            application = Application.objects.create(
                user_id=data.get('user_id'),
                job=job,
                resume=data.get('resume')
            )

            return Response({
                'message': 'Application submitted successfully',
                'application_id': application.id
            }, status=status.HTTP_201_CREATED)

        except Job.DoesNotExist:
            return Response(
                {'message': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request):

        applications = Application.objects.all()

        data = []

        for application in applications:
            data.append({
                'id': application.id,
                'user': application.user.username,
                'job': application.job.title,
                'applied_date': application.applied_date,
                'status': application.status
            })

        return Response(data)
