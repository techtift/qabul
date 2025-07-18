"use client";

import React, { useEffect, useState } from "react";
import ThankYou from "./ThankYou";
import Test from "./test";
import { ApiService } from "@/services/api.service";
import { GET_STUDENT_ENDPOINT } from "@/constants/api";
import { ApiError } from "@/types";
import { toast } from "sonner";
import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";

const Exam = () => {
  const router = useRouter();
    const _t = useTranslations("Messages");

  const [result, setResult] = useState({});
  const [step, setStep] = useState(1);

  useEffect(() => {
    window.scrollTo(0, 0);
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    if(!localStorage.getItem("access_token")) {
      toast(_t("w_login"));
      return router.push("/apply/local-application")
    }
    try {
      const res = await ApiService.get(GET_STUDENT_ENDPOINT, {});
      if (res.data?.is_attended_exam) {
        router.push("/apply/profile");
      }
    } catch (error) {
      const apiError = error as ApiError;
      if(apiError.response?.data?.error_code === "not_found") {
        toast(_t("w_apply"));
        router.push("/apply/local-application");
      }
    }
  };

  const getStepComponent = (step: number) => {
    switch (step) {
      case 1:
        return <Test setStep={setStep} setResult={setResult} />;
      case 2:
        return <ThankYou result={result} />;
      default:
        return null;
    }
  };

  return <>{getStepComponent(step)}</>;
};

export default Exam;
