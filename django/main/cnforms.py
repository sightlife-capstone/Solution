from django import forms
from django.db import connection
import datetime


date_ranges = [
    ("firsthalf", "上半月 (1-15)"),
    ("lasthalf", "下半月 (16-月底)"),
    ("wholemonth", "整整一个月")
]
months = [
    ("01", "一月"),
    ("02", "二月"),
    ("03", "三月"),
    ("04", "四月"),
    ("05", "五月"),
    ("06", "六月"),
    ("07", "七月"),
    ("08", "八月"),
    ("09", "九月"),
    ("10", "十月"),
    ("11", "十一月"),
    ("12", "十二月")
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

class SigninFormCN(forms.Form):
    username = forms.CharField(label='用户名', max_length=30, required=True)
    password = forms.CharField(label='密码', widget=forms.PasswordInput(), max_length=30, required=True)

class partnerMetricMetaDataCN(forms.Form):
    partner = forms.CharField(label="机构名称", widget=forms.Select(choices=getEyebanks()), required=True)
    date_range = forms.CharField(label="日期范围", widget=forms.Select(choices=date_ranges))
    month = forms.CharField(label="月", widget=forms.Select(choices=months))
    year = forms.CharField(label="年", widget=forms.Select(choices=getYear()))


class TotalCorneasCollectedCN(forms.Form):
    total_collected_transplant = forms.IntegerField(label="为移植目的而收集的全眼或角膜", min_value=0, required=True)
    total_distributed = forms.IntegerField(label="用于角膜移植的组织", min_value=0, required=True)

class DeathAndDeathNotificationsCN(forms.Form):
    total_in_hos_deaths = forms.IntegerField(label="HCRP医院的总死亡人数", min_value=0, required=False)
    total_work_hours_deaths = forms.IntegerField(label="在EDC工作时间内，HCRP医院的总死亡人数。",min_value=0, required=False)
    total_death_notifications = forms.IntegerField(label="眼库死亡通知总数",min_value=0, required=False)

class PotentialDonorsAndConsentCN(forms.Form):
    # pd = potential donors
    pd_screened = forms.IntegerField(label="EB工作人员与医生、护士或病历一起审查潜在捐赠者", min_value=0, required=False)
    pd_suitable = forms.IntegerField(label="最初可接受移植的潜在供体", min_value=0, required=False)
    approached_pd = forms.IntegerField(label="在家里捐献的例数", min_value=0, required=False)
    consented_pd = forms.IntegerField(label="在医院捐献例数", min_value=0, required=False)

class TissueRecoveryAndCollectionCN(forms.Form):
    # don = donors, vol = voluntary, ERC = Eye Retrieval Center
    don_hcrp_ebm = forms.IntegerField(label="直接捐献到眼库的捐献者", min_value=0, required=False)
    don_hcrp_opo_hosmotivated = forms.IntegerField(label="来自OPO的捐献者", min_value=0, required=False)
    don_vol = forms.IntegerField(label="来自志愿者介绍的捐献", min_value=0, required=False)
    don_ERC = forms.IntegerField(label="角膜收集中心", min_value=0, required=False)
    don_other = forms.IntegerField(label="其他途径来源", min_value=0, required=False)
    
    corneas_hcrp = forms.IntegerField(label="眼球或眼角膜- HCRP", min_value=0, required=False)
    corneas_vol = forms.IntegerField(label="志愿捐献", min_value=0, required=False)
    corneas_ERC = forms.IntegerField(label="眼球收集中心", min_value=0, required=False)
    corneas_other = forms.IntegerField(label="其他途径的眼角膜", min_value=0, required=False)

    corneas_for_research = forms.IntegerField(label="为研究、训练和其他用途而收集的眼睛/眼角膜总数", min_value=0, required=False)

class EligibilityAndSuitabilityRecoveredTissuesCN(forms.Form): 
    # Reasons not suitable
    donor_elegibility = forms.IntegerField(label="组织不能接受移植的原因: 捐赠的医疗问题", min_value=0, required=False)
    tissue_suitability = forms.IntegerField(label="组织不能接受移植的原因: 组织评估问题(裂隙灯/高光显微镜问题)", min_value=0, required=False)
    other_issues_not_eligible = forms.IntegerField(label="组织不能接受移植的原因: 其他问题", min_value=0, required=False)
    # Tissues suitable
    optical_grade = forms.IntegerField(label="可接受移植的组织: 光学等级(PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_eligible = forms.IntegerField(label="可接受移植的组织: 治疗方式 KLAL, or K-pro only", min_value=0, required=False)
    # Tissues suitable but not distributed
    tissues_expired = forms.IntegerField(label="可接受但不用于移植的组织: 过期的角膜", min_value=0, required=False)

class TissueDistributionCN(forms.Form): 
    # Tissues distributed and used for keratoplasty by type
    optical = forms.IntegerField(label="组织分配并用于角膜移植-按类型: 恢复光学的 (PK, EK, ALK)", min_value=0, required=False)
    therapeutic_tectonic_KLAL_Kpro_distributed = forms.IntegerField(label="组织分配并用于角膜移植-按类型: 仅用于治疗的", min_value=0, required=False)
    # Tissues distributed and used by source
    hcrp_donor_tissue = forms.IntegerField(label="组织的分配和用于角膜移植-按来源: HCRP的角膜使用", min_value=0, required=False)
    vol_donor_tissue = forms.IntegerField(label="组织的分配和用于角膜移植-按来源: 自愿捐献的角膜使用", min_value=0, required=False)
    ERC_donor_tissue = forms.IntegerField(label="组织的分配和用于角膜移植-按来源: 眼球收集中心角膜使用", min_value=0, required=False)
    other_donor_tissue = forms.IntegerField(label="组织的分配和用于角膜移植-按来源: 其他来源的角膜使用", min_value=0, required=False)
    # Tissues distributed for keratoplasty but not used
    distributed_keratoplasty_notused = forms.IntegerField(label="用于角膜移植但未使用的组织", min_value=0, required=False)
    # Tissues ditributed for non-surgical use
    distributed_nonsurgical = forms.IntegerField(label="用于非手术的组织", min_value=0, required=False)
    # EDC Productivity (No of HCRP Transplants/No. of Active EDCs) 
    edc_productivity = forms.IntegerField(label="活动EDC的数量", min_value=0, required=False)
    # Transplants that were recovered as MLC cases
    mlc_recovery_transplants = forms.IntegerField(label="由太平间捐献的角膜恢复的移植", min_value=0, required=False)

class ReasonsTisueNotEligibleTransplantationCN(forms.Form):
    positive_test_communicable_disease = forms.IntegerField(label="Positive or reactive test for communicable disease agent or disease", min_value=0, required=False)
    other_communicable_disease = forms.IntegerField(label="Other communicable disease testing issue", min_value=0, required=False)
    plasma_dilution = forms.IntegerField(label="Plasma Dilution", min_value=0, required=False)
    blood_sample_missing_or_unsuitable = forms.IntegerField(label="Blood Sample unsuitable or missing", min_value=0, required=False)
    medical_record_or_autopsy_findings = forms.IntegerField(label="Medical record or autopsy findings", min_value=0, required=False)
    history_interview_with_family = forms.IntegerField(label="Medical/social/behavioral history interview with family", min_value=0, required=False)
    prior_ocular_history = forms.IntegerField(label="Prior ocular history", min_value=0, required=False)

class ReasonsCorneasNotSuitableTransplantationCN(forms.Form):
    slit_lamp = forms.IntegerField(label="Slit Lamp evaluation", min_value=0, required=False)
    spec_eval = forms.IntegerField(label="Specular evaluation", min_value=0, required=False)
    sterility_media_vial_issue = forms.IntegerField(label="Sterility compromise, media issue, or media vial damage", min_value=0, required=False)
    other_issues_not_suitable = forms.IntegerField(label="Other Issues before distribution", min_value=0, required=False)

class CorneasSuitableNotTransplantedCN(forms.Form):
    tissue_expired_optical = forms.IntegerField(label="Tissue expired - Optical (PK, EK, ALK)", min_value=0, required=False)
    tissue_expired_nonoptical = forms.IntegerField(label="Tissue expired - Non-optical (therapeutic/tectonic, KLAL, or K-Pro only)", min_value=0, required=False)
    surgeon_discards_tissue = forms.IntegerField(label="Suregeon discards tissue (tissue received by surgeon, nut not used)", min_value=0, required=False)
    other_issues_not_transplanted = forms.IntegerField(label="Other issues after distribution", min_value=0, required=False)

class SocialReturnCN(forms.Form):
    free_surgery = forms.IntegerField(label="Total tissues distributed and used for Free surgeries (Surgeon reported", min_value=0, required=False)
    bilaterally_blind_patients = forms.IntegerField(label="Total tissues distributed and used for bilaterally blind patients (Surgeon reported)", min_value=0, required=False)

class IndicationsForTransplantationCN(forms.Form):  
    corneal_scarring = forms.IntegerField(label="Corneal Scarring", min_value=0, required=False)
    acute_inf_keratitis_corneal_ulcers = forms.IntegerField(label="Acute Infectious keratitis / corneal ulcers", min_value=0, required=False)
    regrafting = forms.IntegerField(label="Regrafting", min_value=0, required=False)
    aphakic_bullous_keratopathy = forms.IntegerField(label="Aphakic bullous keratophathy", min_value=0, required=False)
    pseudophakic_bullous_keratophathy = forms.IntegerField(label="Pseudophakic Bullous Keratophathy", min_value=0, required=False)
    fuchs_dystrophy = forms.IntegerField(label="Fuchs Dystrophy", min_value=0, required=False)
    keratoconus = forms.IntegerField(label="Keratoconus", min_value=0, required=False)
    other_degens_or_dystrophies = forms.IntegerField(label="Other degenerations or dystrophies", min_value=0, required=False)
    mechanical_or_chemical_trauma = forms.IntegerField(label="Mechanical or chemical trauma", min_value=0, required=False)
    congenital_opacities = forms.IntegerField(label="Congenital opacities", min_value=0, required=False)
    other_causes_of_opacifications_or_distortion = forms.IntegerField(label="Other causes of corneal opacification or distortion", min_value=0, required=False)
