from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import connection
from calendar import monthrange
import pycountry
from .forms import (
    SigninForm,
    NewEyebankForm,
    partnerMetricMetaData, 
    TotalCorneasCollected,
    DeathAndDeathNotifications, 
    PotentialDonorsAndConsent, 
    TissueRecoveryAndCollection,
    EligibilityAndSuitabilityRecoveredTissues,
    TissueDistribution, 
    ReasonsTisueNotEligibleTransplantation, 
    ReasonsCorneasNotSuitableTransplantation, 
    CorneasSuitableNotTransplanted, 
    SocialReturn, 
    IndicationsForTransplantation,
    GoalsForm,
    MasterForm
)
from .cnforms import (
    SigninFormCN,
    partnerMetricMetaDataCN, 
    TotalCorneasCollectedCN,
    DeathAndDeathNotificationsCN, 
    PotentialDonorsAndConsentCN, 
    TissueRecoveryAndCollectionCN,
    EligibilityAndSuitabilityRecoveredTissuesCN,
    TissueDistributionCN, 
    ReasonsTisueNotEligibleTransplantationCN, 
    ReasonsCorneasNotSuitableTransplantationCN, 
    CorneasSuitableNotTransplantedCN, 
    SocialReturnCN, 
    IndicationsForTransplantationCN
)


def switch_language(request):
    if "Chinese" in request.POST:
        request.session['lang'] = 'cn'
    elif "English" in request.POST:
        request.session['lang'] = 'en'

# Create your views here.
def home(request):
    if request.method == "GET":
        request.session['lang'] = 'en'
        return render(request, 'en-index.html')
    elif request.method == "POST":
        switch_language(request)
        language = request.session['lang']
        template = str(language) + "-index.html"
        return render(request, template)
    else:
        messages.error(request, "That method is not allowed on /", extra_tags="alert alert-warning")


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        if request.user.is_authenticated or request.user.is_staff:
            return HttpResponseRedirect("/form")
        if form.is_valid():
            name = form.cleaned_data['username']
            userPass= form.cleaned_data['password']
            user = authenticate(request, username=name, password=userPass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/form")
            else:
                messages.warning(request, "Invalid Credentials.", extra_tags="alert alert-warning")
        else:
            messages.error(request, "Invalid Credentials.", extra_tags="alert alert-warning")

    elif request.method == "GET":
            language = request.session['lang']
            if language == 'en':
                form = SigninForm()
            else:
                form = SigninFormCN()
    else:
        messages.error(request, "Method not allowed on /signin", extra_tags="alert alert-warning")

    template = request.session['lang'] + "-signin.html"
    return render(request, template, {'form': form})

def form(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/signin")
    elif request.method == "GET":
        if request.session['lang'] == "en":
            form1 = partnerMetricMetaData()
            form2 = TotalCorneasCollected()
            form3 = DeathAndDeathNotifications()
            form4 = PotentialDonorsAndConsent()
            form5 = TissueRecoveryAndCollection()
            form6 = EligibilityAndSuitabilityRecoveredTissues()
            form7 = TissueDistribution()
            form8 = ReasonsTisueNotEligibleTransplantation()
            form9 = ReasonsCorneasNotSuitableTransplantation()
            form10 = CorneasSuitableNotTransplanted()
            form11 = SocialReturn()
            form12 = IndicationsForTransplantation()
            form13 = GoalsForm()
            template = "en-form.html"
        elif request.session['lang'] == "cn":
            form1 = partnerMetricMetaDataCN()
            form2 = TotalCorneasCollectedCN()
            form3 = DeathAndDeathNotificationsCN()
            form4 = PotentialDonorsAndConsentCN()
            form5 = TissueRecoveryAndCollectionCN()
            form6 = EligibilityAndSuitabilityRecoveredTissuesCN()
            form7 = TissueDistributionCN()
            form8 = ReasonsTisueNotEligibleTransplantationCN()
            form9 = ReasonsCorneasNotSuitableTransplantationCN()
            form10 = CorneasSuitableNotTransplantedCN()
            form11 = SocialReturnCN()
            form12 = IndicationsForTransplantationCN()
            form13 = GoalsForm()
            template = "cn-form.html"
        return render(request, template, {'form1': form1,
                                             'form2' : form2,
                                             'form3' : form3,
                                             'form4' : form4,
                                             'form5' : form5,
                                             'form6' : form6,
                                             'form7' : form7,
                                             'form8' : form8,
                                             'form9' : form9,
                                             'form10' : form10,
                                             'form11' : form11,
                                             'form12' : form12,
                                             'form13' : form13}, status=200)
    
    elif request.method == "POST":
        form = MasterForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            eyebank_id = form.cleaned_data['partner']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            date_range = form.cleaned_data['date_range']

            #Specify the date range for the data being submitted
            #If the date range is the first half of the month, then the date range should be 1st through 15th
            #If the date range is the last half of the month, then the date range should be 16th through 28/30/31
            #If the date range is the whole month, then the date range should be 1st through 28/30/31 (Note does account for leap years)
            start_day = 1
            if date_range == "lasthalf":
                start_day = 16
            end_of_month = monthrange(int(year), int(month))
            end_day = end_of_month[1]
            if date_range == "firsthalf":
                end_day = 15
            start_date = str(year) + "-" + str(month) + "-" + str(start_day)
            end_date = str(year) + "-" + str(month) + "-" + str(end_day)
        
            # Assuming we use the exact label from the field for the name in the database, iterate over all the fields in the form
            for field in form:
                # Ignore the first fields in the form for they are metadata that is not being submitted
                if field.name == "partner" or field.name == "month" or field.name == "year" or field.name == "date_range":
                    pass
                # For each field, if the field was filled out, we get the fields id from the database and then add a row to the table eyebank_metric
                elif form.cleaned_data[field.name] is not None:
                    cursor.execute("SELECT metric.metricid FROM Metric WHERE metricname=%s;", [field.label])
                    data = cursor.fetchall()
                    try: # if data has been already submitted for a field, update it
                        cursor.execute("UPDATE eyebank_metric SET measure = %s, startdate = %s, enddate = %s WHERE eyebankid = %s AND metricid= %s;", 
                            [form.cleaned_data[field.name], start_date, end_date, eyebank_id, data[0][0]]
                        )
                    except: # If the data has not yet been submitted for a field, insert it
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                                        [eyebank_id, data[0][0], form.cleaned_data[field.name], start_date, end_date]
                        )

            # Compute the rate information for hcrp utilization
            if form.cleaned_data["hcrp_donor_tissue"] is not None and form.cleaned_data["corneas_hcrp"] is not None:
                if form.cleaned_data["corneas_hcrp"] != 0:
                    hcrp_utilization_rate = form.cleaned_data["hcrp_donor_tissue"] / form.cleaned_data["corneas_hcrp"]
                    cursor.execute("SELECT metric.metricid FROM metric WHERE metricname = %s;", ["HCRP Utilization Rate"])
                    metric_id = cursor.fetchone()[0]
                    try:
                        cursor.execute("UPDATE eyebank_metric SET measure = %s WHERE eyebankid = %s AND metricid = %s AND startdate = %s AND enddate = %s;", 
                            [hcrp_utilization_rate, eyebank_id, metric_id, start_date, end_date]
                        )
                    except:
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                            [eyebank_id, metric_id, hcrp_utilization_rate, start_date, end_date]
                        )
            # Compute the rate information for notification
            if form.cleaned_data["total_work_hours_deaths"] is not None and form.cleaned_data["total_in_hos_deaths"] is not None:
                if form.cleaned_data["total_in_hos_deaths"] != 0:
                    notifications_rate = form.cleaned_data["total_work_hours_deaths"] / form.cleaned_data["total_in_hos_deaths"]
                    cursor.execute("SELECT metric.metricid FROM metric WHERE metricname = %s;", ["Notification Rate"])
                    metric_id = cursor.fetchone()[0]
                    try:
                        cursor.execute("UPDATE eyebank_metric SET measure = %s WHERE eyebankid = %s AND metricid = %s AND startdate = %s AND enddate = %s;", 
                            [notifications_rate, eyebank_id, metric_id, start_date, end_date]
                        )
                    except:
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                            [eyebank_id, metric_id, notifications_rate, start_date, end_date]
                        )
            # Compute the rate information for tissue suitability
            if form.cleaned_data["pd_screened"] is not None and form.cleaned_data["pd_suitable"] is not None:
                if form.cleaned_data["pd_suitable"] != 0:
                    suitability_rate = form.cleaned_data["pd_screened"] / form.cleaned_data["pd_suitable"]
                    cursor.execute("SELECT metric.metricid FROM metric WHERE metricname = %s;", ["Suitability Rate"])
                    metric_id = cursor.fetchone()[0]
                    try:
                        cursor.execute("UPDATE eyebank_metric SET measure = %s WHERE eyebankid = %s AND metricid = %s AND startdate = %s AND enddate = %s;", 
                            [suitability_rate, eyebank_id, metric_id, start_date, end_date]
                        )
                    except:
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                            [eyebank_id, metric_id, suitability_rate, start_date, end_date]
                        )
            # Compute the rate information for approachment
            if form.cleaned_data["consented_pd"] is not None and form.cleaned_data["approached_pd"] is not None:
                if form.cleaned_data["approached_pd"] != 0:
                    consent_rate = form.cleaned_data["consented_pd"] / form.cleaned_data["approached_pd"]
                    cursor.execute("SELECT metric.metricid FROM metric WHERE metricname = %s;", ["Consent Rate"])
                    metric_id = cursor.fetchone()[0]
                    try:
                        cursor.execute("UPDATE eyebank_metric SET measure = %s WHERE eyebankid = %s AND metricid = %s AND startdate = %s AND enddate = %s;", 
                            [consent_rate, eyebank_id, metric_id, start_date, end_date]
                        )
                    except:
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                            [eyebank_id, metric_id, consent_rate, start_date, end_date]
                        )
            # Compute the rate information for edc productivity
            if form.cleaned_data["hcrp_donor_tissue"] is not None and form.cleaned_data["num_active_edc"] is not None:
                if form.cleaned_data["num_active_edc"] != 0:
                    edc_productivity = form.cleaned_data["hcrp_donor_tissue"] / form.cleaned_data["num_active_edc"]
                    cursor.execute("SELECT metric.metricid FROM metric WHERE metricname = %s;", ["EDC Productivity"])
                    metric_id = cursor.fetchone()[0]
                    try:
                        cursor.execute("UPDATE eyebank_metric SET measure = %s WHERE eyebankid = %s AND metricid = %s AND startdate = %s AND enddate = %s;", 
                            [consent_rate, eyebank_id, metric_id, start_date, end_date]
                        )
                    except:
                        cursor.execute("INSERT INTO eyebank_metric (eyebankid, metricid, measure, startdate, enddate) VALUES (%s, %s, %s, %s, %s)",
                            [eyebank_id, metric_id, edc_productivity, start_date, end_date]
                        )
           
            cursor.close()
            # Return a success a link to logout the user
            response = HttpResponse()
            if request.session['lang'] == "en":
                response.write("<p>Success!</p>")
                response.write("<a href='/signout'>Sign Out</a>")
            elif request.session['lang'] == "cn":
                response.write("<p>成功！</p>")
                response.write("<a href='/signout'>登出</a>")
            return response
        else:
            messages.error(request, "Error submitting the form", extra_tags="alert alert-warning")
    else:
        messages.error(request, "Method not allowed on /form", extra_tags="alert alert-warning")

def signout(request):
    '''Signs out a user if they are logged into the system'''
    if request.method == "GET":
        if request.user.is_authenticated:
           logout(request)
           return HttpResponseRedirect("/")
        else:
            return HttpResponse("Not logged in.", status=200)
    else:
        messages.error(request, "Method not allowed on /form", extra_tags="alert alert-warning")


def additions(request):
    '''Allows staff members to add new Eyebanks to the database'''
    if not request.user.is_staff:
        return HttpResponseRedirect("/")
    if request.method == "GET":
        form = NewEyebankForm()
        return render(request, 'additions.html', {'form': form})
    elif request.method == "POST":
        form = NewEyebankForm(request.POST)
        if form.is_valid():
            cursor = connection.cursor()
            # Get full name of country since only a code is returned
            country_name = pycountry.countries.get(alpha_2=form.cleaned_data["country"]).name
            # If inserting an eyebank in a new country, that country will be added to the database with the selected partner grouping
            if form.cleaned_data["partner_group"] != "":
                partner_group_id = form.cleaned_data["partner_group"]
                # This is to ensure that no country already in the database is added again
                cursor.execute("SELECT * FROM country WHERE countryname = %s", [country_name])
                data = cursor.fetchone()
                if data is None:
                    cursor.execute("INSERT INTO country (partnergroupid, countryname) VALUES (%s, %s);", 
                        [partner_group_id, form.cleaned_data["country"]]
                    )
            # Get the country id from the database
            cursor.execute("SELECT countryid FROM country WHERE countryname = %s;", [country_name])
            countryid = cursor.fetchone()[0]
            # Insert the new eyebank into the database
            try:
                cursor.execute("UPDATE eye_bank SET countryid = %s , eyebankshortname = %s , eyebankfullname = %s WHERE OR eyebankshortname = %s OR eyebankfullname = %s;", 
                    [countryid, form.cleaned_data["short_name"], form.cleaned_data["full_name"], form.cleaned_data["short_name"], form.cleaned_data["full_name"]]
                )
            except:
                cursor.execute("INSERT INTO eye_bank (countryid, eyebankshortname, eyebankfullname) VALUES (%s, %s, %s);", 
                    [countryid, form.cleaned_data["short_name"], form.cleaned_data["full_name"]]
                )
            cursor.close()
            messages.info(request, "Eyebank added to the database")
            return HttpResponseRedirect("/additions")
        else:
            messages.error(request, "Invalid form input", extra_tags="alert alert-warning")
    else:
        messages.error(request, "Method not allowed on /additions", extra_tags="alert alert-warning")