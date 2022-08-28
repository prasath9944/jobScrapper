from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as urReq

app = Flask(__name__)

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")


@app.route('/findjob',methods=["GET","POST"])
def find_Job():
    if request.method=='POST':
        name=request.form.get("Name")
        role=request.form.get("role")
        location=request.form.get('location')
        experience=request.form.get('experience')
        flipkart_url="https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={role}&txtLocation={location}&cboWorkExp1={experience}".format(role=role,location=location,experience=experience)
        response_website=urReq(flipkart_url)
        data_flipkart=response_website.read()
        beautified_html=bs(data_flipkart,"html.parser")
        bigbox=beautified_html.find_all("li",{"class":"clearfix job-bx wht-shd-bx"})
        job_description=beautified_html.find_all("ul",{"class":"list-job-dtl clearfix"})
        tech_skills=beautified_html.find_all("span",{"class":"srp-skills"})[0].text.strip()
        tech_skills_ls=[]
        job_description_ls=[]
        location_ls=[]
        exp_years_ls=[]
        job_role_url_ls=[]
        job_role_ls=[]
        company_name_ls=[]
        for i in range(len(bigbox)):
            job_role = bigbox[i].header.h2.a.text.strip()
            tech_skills = beautified_html.find_all("span", {"class": "srp-skills"})[i].text.strip()
            description = job_description[i].li.text.strip()[18:]
            exp_years = bigbox[i].ul.li.text[11:]
            company_name = bigbox[i].header.h3.text.strip()
            job_role_url = bigbox[i].header.h2.a['href']
            location = bigbox[i].ul.span.text

            tech_skills_ls.append(tech_skills)
            job_description_ls.append(description)
            location_ls.append(location)
            exp_years_ls.append(exp_years)
            job_role_url_ls.append(job_role_url)
            job_role_ls.append(job_role)
            company_name_ls.append(company_name)
        final_len=len(tech_skills_ls)
    return render_template('job.html',company_name=company_name_ls,skills=tech_skills_ls,job_description=job_description_ls,experience_level=exp_years_ls,length=final_len,name=name,location=location_ls,jobrole=role,url=job_role_url_ls)
    # return render_template('sample.html',company_name=company_name_ls)

if __name__=='__main__':
    app.run(debug=True)