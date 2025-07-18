"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import ApplicationSteps from "@/components/ApplicationSteps";
import Step1 from "@/app/[locale]/apply/local-application/components/Step1";
import Step2 from "@/app/[locale]/apply/local-application/components/Step2";
import Step3 from "@/app/[locale]/apply/local-application/components/Step3";
import Step4 from "@/app/[locale]/apply/local-application/components/Step4";
import ThankYou from "./components/ThankYou";
// import { getCurrentYear } from "@/utils/date";
import Breadcrumb from "@/components/Breadcumb";
import { StudentApplicationData } from "@/types";
import { useTranslations } from "next-intl";

const LocalApplication = () => {
  const t = useTranslations("LocalApplication");

  const [userId, setUserId] = useState<number | null>(null);

  useEffect(() => {
    // This code runs only on the client side
    const user = localStorage.getItem("user");
    setUserId(user ? JSON.parse(user).id : null);
  }, []);
  const [step, setStep] = useState(1);
  const [data, setData] = useState<StudentApplicationData>({
    student_id: null,
    application_id: null,
    program_id: null,
    faculty_id: null,
    is_transfer: false,
    user_id: userId,
    study_type_id: null,
    is_online_exam: false,
    exam_date_id: null,
    transfer_level: null,
    transcript: null,
  });

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      setStep(2);
    }
  }, []);

  const getStepComponent = (step: number) => {
    switch (step) {
      case 1:
        return <Step1 setStep={setStep} data={data} setData={setData} />;
      case 2:
        return <Step2 setStep={setStep} data={data} setData={setData} />;
      case 3:
        return <Step3 setStep={setStep} data={data} setData={setData} />;
      case 4:
        return <Step4 setStep={setStep} data={data} setData={setData} />;
      case 5:
        return <ThankYou />;
      default:
        return null;
    }
  };
  return (
    <>
      <Breadcrumb />
      <div className="custom-container xl:px-40">
        {/* Page Title */}
        <h1 className="title">
          {/* Application for the {getCurrentYear()}-{getCurrentYear() + 1} academic year */}
          {t("title")}
        </h1>

        {step !== 5 && (
          <Card className="shadow-none border-none px-0 py-2">
            <CardContent className="px-0 py-0">
              <ApplicationSteps step={step} />
            </CardContent>
          </Card>
        )}

        <Card className={`shadow-none border-none ${step === 5 ? "px-0 py-0" : "py-2"}`}>
          <CardContent
            className={`space-y-8 text-start ${step === 5 ? "px-0 py-0" : "px-6 py-0 md:py-4"}`}>
            {getStepComponent(step)}
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default LocalApplication;
