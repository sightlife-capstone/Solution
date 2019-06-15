from django import forms
from django.db import connection
import datetime
from django_countries.fields import CountryField


date_ranges = [
    ("firsthalf", "First half of the month (1-15)"),
    ("lasthalf", "Last half of the month (16-End of Month)"),
    ("wholemonth", "Whole month")
]
months = [
    ("01", "January"),
    ("02", "February"),
    ("03", "March"),
    ("04", "April"),
    ("05", "May"),
    ("06", "June"),
    ("07", "July"),
    ("08", "August"),
    ("09", "Spetember"),
    ("10", "October"),
    ("11", "November"),
    ("12", "December")
]


def getYear():
    today = datetime.date.today().year
    years = [(str(today), str(today)), (str(today - 1), str(today - 1))]
    return years

def getEyebanks():
    cursor = connection.cursor()
    cursor.execute("SELECT eye_bank.eyebankid, eye_bank.eyebankfullname FROM eye_bank")
    data = cursor.fetchall()
    cursor.close()
    return data

def getPartnerGroups():
    cursor = connection.cursor()
    empty = [("", "")]
    cursor.execute("SELECT * FROM partner_group;")
    data = cursor.fetchall()
    for each in data:
        empty.append(each)
    cursor.close()
    return empty

class SigninForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), max_length=30, required=True)

class NewEyebankForm(forms.Form):
    short_name = forms.CharField(label="Eyebank short name to be viewed in the data analysis", max_length=30, required=True)
    full_name = forms.CharField(label="Eyebank full name for eyebanks to select from in the form", max_length=255, required=True)
    country = CountryField().formfield()
    partner_group = forms.CharField(label="If you are adding an eyebank in a brand new country, select which partner group you want that country to be a part of", widget=forms.Select(choices=getPartnerGroups()), required=False)

class partnerMetricMetaData(forms.Form):
    partner = forms.CharField(label="Eyebank Name", widget=forms.Select(choices=getEyebanks()), required=True)
    date_range = forms.CharField(label="Date range of data being submitted", widget=forms.Select(choices=date_ranges))
    month = forms.CharField(label="Month", widget=forms.Select(choices=months))
    year = forms.CharField(label="Year", widget=forms.Select(choices=getYear()))


class TotalCorneasCollected(forms.Form):
    total_collected_transplant = forms.IntegerField(label="Total eyes or corneas recovered with intent for transplant", min_value=0, required=True)
    total_distributed = forms.IntegerField(label="Total tissues distributed and used for keratoplasty", min_value=0, required=True)

class DeathAndDeathNotifications(forms.Form):
    total_in_hos_deaths = forms.IntegerField(label="Total deaths in hospitals served", min_value=0, required=False)
    total_work_hours_deaths = forms.IntegerField(label="Total deaths in units served during working hours",min_value=0, required=False)
    total_death_notifications = forms.IntegerField(label="Total death notifications to the eye bank",min_value=0, required=False)

class PotentialDonorsAndConsent(forms.Form):
    # pd = potential donors
    pd_screened = forms.IntegerField(label="Potential donors screened by EB staff with doctor, nurse, or medical chart", min_value=0, required=False)
    pd_suitable = forms.IntegerField(label="Potential Donors initially suitable for transplant", min_value=0, required=False)
    approached_pd = forms.IntegerField(label="Approached potential donors", min_value=0, required=False)
    consented_pd = forms.IntegerField(label="Consented potential donors - HCRP", min_value=0, required=False)

class TissueRecoveryAndCollection(forms.Form):
    # don = donors, vol = voluntary, ERC = Eye Retrieval Center
    don_hcrp_ebm = forms.IntegerField(label="Donors - HCRP (Eye Bank Motivated)", min_value=0, required=False)
    don_hcrp_opo_hosmotivated = forms.IntegerField(label="Donors - HCRP (OPO/Hospital motivated)", min_value=0, required=False)
    don_vol = forms.IntegerField(label="Donors - Voluntary", min_value=0, required=False)
    don_ERC = forms.IntegerField(label="Donors - Eye Retrieval Centers", min_value=0, required=False)
    don_other = forms.IntegerField(label="Donors - Other Sources", min_value=0, required=False)
    
    corneas_hcrp = forms.IntegerField(label="Eyes or corneas - HCRP", min_value=0, required=False)
    corneas_vol = forms.IntegerField(label="Eyes or corneas - Voluntary", min_value=0, required=False)
    corneas_ERC = forms.IntegerField(label="Eyes or corneas - Eye Retrieval Centers", min_value=0, required=False)
    corneas_other = forms.IntegerField(label="Eyes or corneas - Other Sources", min_value=0, required=False)

    corneas_for_research = forms.IntegerField(label="Total Eyes/corneas recovered with intent for research, training, and other uses - All sources", min_value=0, required=False)

class EligibilityAndSuitabilityRecoveredTissues(forms.Form): 
    # Reasons not suitable
    donor_elegibility = forms.IntegerField(label="Not suitable - Donor eligibility (medical history, serology, etc.)", min_value=0, required=False)
    tissue_suitability = forms.IntegerField(label="Not suitable - Tissue Suitability (specular/slit-lamp)", min_value=0, required=False)
    other_issues_not_eligible = forms.IntegerField(label="Not suitable - Other issues", min_value=0, required=False)
    # Tissues suitable
    optical_grade = forms.IntegerField(label="Suitable - Optical grade (PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_eligible = forms.IntegerField(label="Suitable - Therapeutic, tectonic, KLAL, or K-pro only", min_value=0, required=False)
    # Tissues suitable but not distributed
    tissues_expired = forms.IntegerField(label="Suitable / Not distributed - Tissue Expired", min_value=0, required=False)

class TissueDistribution(forms.Form): 
    # Tissues distributed and used for keratoplasty by type
    optical = forms.IntegerField(label="Distributed and used / Type - Optical (PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_distributed = forms.IntegerField(label="Distributed and used / Type - Therapeutic, tectonic, KLAL, or K-pro only", min_value=0, required=False)
    # Tissues distributed and used by source
    hcrp_donor_tissue = forms.IntegerField(label="Distributed and used / Source - HCRP donor tissue used", min_value=0, required=False)
    vol_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Voluntary donor tissue used", min_value=0, required=False)
    ERC_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Eye Retrieval Center donor tissue used", min_value=0, required=False)
    other_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Other sourced donor tissue used", min_value=0, required=False)
    # Tissues distributed for keratoplasty but not used
    distributed_keratoplasty_notused = forms.IntegerField(label="Tissues distributed for keratoplasty but not used", min_value=0, required=False)
    # Tissues ditributed for non-surgical use
    distributed_nonsurgical = forms.IntegerField(label="Tissues distributed for non-surgical use", min_value=0, required=False)
    # Number of active EDC's
    num_active_edc = forms.IntegerField(label="Number of Active EDCs", min_value=0, required=False)
    # Transplants that were recovered as MLC cases
    mlc_recovery_transplants = forms.IntegerField(label="Transplants that were recovered as MLC cases", min_value=0, required=False)

class ReasonsTisueNotEligibleTransplantation(forms.Form):
    hiv_antibody = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - HIV Antibody", min_value=0, required=False)
    hepatitis_b_surface_antigen = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Hepatitis B Surface Antigen (HBsAg)", min_value=0, required=False)
    hepatitis_c_antibody = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Hepatitis C Antibody", min_value=0, required=False)
    syphilis_vdrl = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Syphilis/VDRL", min_value=0, required=False)
    other_communicable_disease_pos_test = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Other positive or reactive test for communicable disease", min_value=0, required=False)
    other_communicable_disease = forms.IntegerField(label="Other communicable disease testing issue", min_value=0, required=False)
    plasma_dilution = forms.IntegerField(label="Plasma Dilution", min_value=0, required=False)
    blood_sample_missing_or_unsuitable = forms.IntegerField(label="Blood Sample unsuitable or missing", min_value=0, required=False)
    medical_record_or_autopsy_findings = forms.IntegerField(label="Medical record or autopsy findings", min_value=0, required=False)
    history_interview_with_family = forms.IntegerField(label="Medical/social/behavioral history interview with family", min_value=0, required=False)
    prior_ocular_history = forms.IntegerField(label="Prior ocular history", min_value=0, required=False)

class ReasonsCorneasNotSuitableTransplantation(forms.Form):
    slit_lamp = forms.IntegerField(label="Slit Lamp evaluation", min_value=0, required=False)
    spec_eval = forms.IntegerField(label="Specular evaluation", min_value=0, required=False)
    sterility_media_vial_issue = forms.IntegerField(label="Sterility compromise, media issue, or media vial damage", min_value=0, required=False)
    other_issues_not_suitable = forms.IntegerField(label="Other Issues before distribution", min_value=0, required=False)

class CorneasSuitableNotTransplanted(forms.Form):
    tissue_expired_optical = forms.IntegerField(label="Tissue expired - Optical (PK, EK, ALK)", min_value=0, required=False)
    tissue_expired_nonoptical = forms.IntegerField(label="Tissue expired - Non-optical (therapeutic/tectonic, KLAL, or K-Pro only)", min_value=0, required=False)
    surgeon_discards_tissue = forms.IntegerField(label="Suregeon discards tissue (tissue received by surgeon, nut not used)", min_value=0, required=False)
    other_issues_not_transplanted = forms.IntegerField(label="Other issues after distribution", min_value=0, required=False)

class SocialReturn(forms.Form):
    free_surgery = forms.IntegerField(label="Total tissues distributed and used for Free surgeries (Surgeon reported)", min_value=0, required=False)
    bilaterally_blind_patients = forms.IntegerField(label="Total tissues distributed and used for bilaterally blind patients (Surgeon reported)", min_value=0, required=False)

class IndicationsForTransplantation(forms.Form):  
    corneal_scarring = forms.IntegerField(label="Corneal scarring", min_value=0, required=False)
    acute_inf_keratitis_corneal_ulcers = forms.IntegerField(label="Acute infectious keratitis / corneal ulcers", min_value=0, required=False)
    regrafting = forms.IntegerField(label="Regrafting", min_value=0, required=False)
    aphakic_bullous_keratopathy = forms.IntegerField(label="Aphakic bullous keratophathy", min_value=0, required=False)
    pseudophakic_bullous_keratophathy = forms.IntegerField(label="Pseudophakic bullous keratophathy", min_value=0, required=False)
    fuchs_dystrophy = forms.IntegerField(label="Fuchs dystrophy", min_value=0, required=False)
    keratoconus = forms.IntegerField(label="Keratoconus", min_value=0, required=False)
    other_degens_or_dystrophies = forms.IntegerField(label="Other degenerations or dystrophies", min_value=0, required=False)
    mechanical_or_chemical_trauma = forms.IntegerField(label="Mechanical or chemical trauma", min_value=0, required=False)
    congenital_opacities = forms.IntegerField(label="Congenital opacities", min_value=0, required=False)
    other_causes_of_opacifications_or_distortion = forms.IntegerField(label="Other causes of corneal opacification or distortion", min_value=0, required=False)

class GoalsForm(forms.Form):
    # Target fields as requested by Julien
    total_transplant_target = forms.IntegerField(label="Total Transplant Target", min_value=0, required=False)
    hcrp_transplant_target = forms.IntegerField(label="Total HCRP Target", min_value=0, required=False)


class MasterForm(forms.Form):
    partner = forms.CharField(label="Eyebank Name", widget=forms.Select(choices=getEyebanks()), required=True)
    date_range = forms.CharField(label="Date range of data being submitted", widget=forms.Select(choices=date_ranges))
    month = forms.CharField(label="Month", widget=forms.Select(choices=months))
    year = forms.CharField(label="Year", widget=forms.Select(choices=getYear()))
    total_collected_transplant = forms.IntegerField(label="Total eyes or corneas recovered with intent for transplant", min_value=0, required=True)
    total_distributed = forms.IntegerField(label="Total tissues distributed and used for keratoplasty", min_value=0, required=True)

    total_in_hos_deaths = forms.IntegerField(label="Total deaths in hospitals served", min_value=0, required=False)
    total_work_hours_deaths = forms.IntegerField(label="Total deaths in units served during working hours",min_value=0, required=False)
    total_death_notifications = forms.IntegerField(label="Total death notifications to the eye bank",min_value=0, required=False)

    # pd = potential donors
    pd_screened = forms.IntegerField(label="Potential donors screened by EB staff with doctor, nurse, or medical chart", min_value=0, required=False)
    pd_suitable = forms.IntegerField(label="Potential Donors initially suitable for transplant", min_value=0, required=False)
    approached_pd = forms.IntegerField(label="Approached potential donors", min_value=0, required=False)
    consented_pd = forms.IntegerField(label="Consented potential donors - HCRP", min_value=0, required=False)

    # don = donors, vol = voluntary, ERC = Eye Retrieval Center
    don_hcrp_ebm = forms.IntegerField(label="Donors - HCRP (Eye Bank Motivated)", min_value=0, required=False)
    don_hcrp_opo_hosmotivated = forms.IntegerField(label="Donors - HCRP (OPO/Hospital motivated)", min_value=0, required=False)
    don_vol = forms.IntegerField(label="Donors - Voluntary", min_value=0, required=False)
    don_ERC = forms.IntegerField(label="Donors - Eye Retrieval Centers", min_value=0, required=False)
    don_other = forms.IntegerField(label="Donors - Other Sources", min_value=0, required=False)
    
    corneas_hcrp = forms.IntegerField(label="Eyes or corneas - HCRP", min_value=0, required=False)
    corneas_vol = forms.IntegerField(label="Eyes or corneas - Voluntary", min_value=0, required=False)
    corneas_ERC = forms.IntegerField(label="Eyes or corneas - Eye Retrieval Centers", min_value=0, required=False)
    corneas_other = forms.IntegerField(label="Eyes or corneas - Other Sources", min_value=0, required=False)

    corneas_for_research = forms.IntegerField(label="Total Eyes/corneas recovered with intent for research, training, and other uses - All sources", min_value=0, required=False)

    # Reasons not suitable
    donor_elegibility = forms.IntegerField(label="Not suitable - Donor eligibility (medical history, serology, etc.)", min_value=0, required=False)
    tissue_suitability = forms.IntegerField(label="Not suitable - Tissue Suitability (specular/slit-lamp)", min_value=0, required=False)
    other_issues_not_eligible = forms.IntegerField(label="Not suitable - Other issues", min_value=0, required=False)
    # Tissues suitable
    optical_grade = forms.IntegerField(label="Suitable - Optical grade (PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_eligible = forms.IntegerField(label="Suitable - Therapeutic, tectonic, KLAL, or K-pro only", min_value=0, required=False)
    # Tissues suitable but not distributed
    tissues_expired = forms.IntegerField(label="Suitable / Not distributed - Tissue Expired", min_value=0, required=False)

   # Tissues distributed and used for keratoplasty by type
    optical = forms.IntegerField(label="Distributed and used / Type - Optical (PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_distributed = forms.IntegerField(label="Distributed and used / Type - Therapeutic, tectonic, KLAL, or K-pro only", min_value=0, required=False)
    # Tissues distributed and used by source
    hcrp_donor_tissue = forms.IntegerField(label="Distributed and used / Source - HCRP donor tissue used", min_value=0, required=False)
    vol_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Voluntary donor tissue used", min_value=0, required=False)
    ERC_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Eye Retrieval Center donor tissue used", min_value=0, required=False)
    other_donor_tissue = forms.IntegerField(label="Distributed and used / Source - Other sourced donor tissue used", min_value=0, required=False)
    # Tissues distributed for keratoplasty but not used
    distributed_keratoplasty_notused = forms.IntegerField(label="Tissues distributed for keratoplasty but not used", min_value=0, required=False)
    # Tissues ditributed for non-surgical use
    distributed_nonsurgical = forms.IntegerField(label="Tissues distributed for non-surgical use", min_value=0, required=False)
    # Number of active EDC's
    num_active_edc = forms.IntegerField(label="Number of Active EDCs", min_value=0, required=False)
    # Transplants that were recovered as MLC cases
    mlc_recovery_transplants = forms.IntegerField(label="Transplants that were recovered as MLC cases", min_value=0, required=False)

    hiv_antibody = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - HIV Antibody", min_value=0, required=False)
    hepatitis_b_surface_antigen = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Hepatitis B Surface Antigen (HBsAg)", min_value=0, required=False)
    hepatitis_c_antibody = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Hepatitis C Antibody", min_value=0, required=False)
    syphilis_vdrl = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Syphilis/VDRL", min_value=0, required=False)
    other_communicable_disease_pos_test = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease - Other positive or reactive test for communicable disease", min_value=0, required=False)
    other_communicable_disease = forms.IntegerField(label="Other communicable disease testing issue", min_value=0, required=False)
    plasma_dilution = forms.IntegerField(label="Plasma Dilution", min_value=0, required=False)
    blood_sample_missing_or_unsuitable = forms.IntegerField(label="Blood Sample unsuitable or missing", min_value=0, required=False)
    medical_record_or_autopsy_findings = forms.IntegerField(label="Medical record or autopsy findings", min_value=0, required=False)
    history_interview_with_family = forms.IntegerField(label="Medical/social/behavioral history interview with family", min_value=0, required=False)
    prior_ocular_history = forms.IntegerField(label="Prior ocular history", min_value=0, required=False)

    slit_lamp = forms.IntegerField(label="Slit Lamp evaluation", min_value=0, required=False)
    spec_eval = forms.IntegerField(label="Specular evaluation", min_value=0, required=False)
    sterility_media_vial_issue = forms.IntegerField(label="Sterility compromise, media issue, or media vial damage", min_value=0, required=False)
    other_issues_not_suitable = forms.IntegerField(label="Other Issues before distribution", min_value=0, required=False)

    tissue_expired_optical = forms.IntegerField(label="Tissue expired - Optical (PK, EK, ALK)", min_value=0, required=False)
    tissue_expired_nonoptical = forms.IntegerField(label="Tissue expired - Non-optical (therapeutic/tectonic, KLAL, or K-Pro only)", min_value=0, required=False)
    surgeon_discards_tissue = forms.IntegerField(label="Suregeon discards tissue (tissue received by surgeon, nut not used)", min_value=0, required=False)
    other_issues_not_transplanted = forms.IntegerField(label="Other issues after distribution", min_value=0, required=False)

    free_surgery = forms.IntegerField(label="Total tissues distributed and used for Free surgeries (Surgeon reported)", min_value=0, required=False)
    bilaterally_blind_patients = forms.IntegerField(label="Total tissues distributed and used for bilaterally blind patients (Surgeon reported)", min_value=0, required=False)

    corneal_scarring = forms.IntegerField(label="Corneal scarring", min_value=0, required=False)
    acute_inf_keratitis_corneal_ulcers = forms.IntegerField(label="Acute infectious keratitis / corneal ulcers", min_value=0, required=False)
    regrafting = forms.IntegerField(label="Regrafting", min_value=0, required=False)
    aphakic_bullous_keratopathy = forms.IntegerField(label="Aphakic bullous keratophathy", min_value=0, required=False)
    pseudophakic_bullous_keratophathy = forms.IntegerField(label="Pseudophakic bullous keratophathy", min_value=0, required=False)
    fuchs_dystrophy = forms.IntegerField(label="Fuchs dystrophy", min_value=0, required=False)
    keratoconus = forms.IntegerField(label="Keratoconus", min_value=0, required=False)
    other_degens_or_dystrophies = forms.IntegerField(label="Other degenerations or dystrophies", min_value=0, required=False)
    mechanical_or_chemical_trauma = forms.IntegerField(label="Mechanical or chemical trauma", min_value=0, required=False)
    congenital_opacities = forms.IntegerField(label="Congenital opacities", min_value=0, required=False)
    other_causes_of_opacifications_or_distortion = forms.IntegerField(label="Other causes of corneal opacification or distortion", min_value=0, required=False)
    # Target fields as requested by Julien
    total_transplant_target = forms.IntegerField(label="Total Transplant Target", min_value=0, required=False)
    hcrp_transplant_target = forms.IntegerField(label="Total HCRP Target", min_value=0, required=False)

