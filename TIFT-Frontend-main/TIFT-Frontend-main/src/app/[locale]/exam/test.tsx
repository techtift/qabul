"use client";

import Breadcrumb from "@/components/Breadcumb";
import { Button } from "@/components/ui/button";
import { EXAM_QUESTION_CHECK, GET_EXAM_QUESTION } from "@/constants/api";
import { ApiService } from "@/services/api.service";
import { useTranslations } from "next-intl";
import Link from "next/link";
import React, { useEffect, useState } from "react";
import { toast } from "sonner";

type Question = {
  id: string | number;
  question_text: string;
  version_a: string;
  version_b: string;
  version_c: string;
  version_d: string;
};
type Subject = {
  subject_id: string | number;
  subject_name: string;
  questions?: Question[];
};

const Test = ({setStep,setResult,}: {
  setStep: (step: number) => void;
  setResult: (result: object) => void;
}) => {
  const t = useTranslations("Exam");
  const $t = useTranslations("Messages");

  const [selectedAnswers, setSelectedAnswers] = useState<{
    [key: string]: string;
  }>({});
  const [data, setData] = useState<Subject[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await ApiService.get(GET_EXAM_QUESTION, {});
      setData(response.data);
    } catch (error) {
      // console.error("Error fetching exam data:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const submitExam = async () => {
    // const totalQuestions = data.reduce((acc, subject) => acc + (subject.questions?.length || 0), 0);
    // if (Object.keys(selectedAnswers).length < totalQuestions) {
    //   toast.error("Iltimos, barcha savollarga javob bering!");
    //   return;
    // }

    const payload = Object.entries(selectedAnswers).map(
      ([question_id, selected]) => ({
        question_id: Number(question_id),
        selected,
      })
    );
    try {
      const response = await ApiService.post(EXAM_QUESTION_CHECK, payload);
      if (response.status === 200) {
        setResult(response.data);
        toast($t("s_exam_submit"));
        setStep(2);
      }
    } catch (error) {
      // console.error("Error submitting exam:", error);
      toast($t("e_unexpected_error"));
    }
  };

  return (
    <>
      <Breadcrumb />
      <div className="custom-container">
        <h1 className="title">
          {t("title")}
        </h1>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="text-center text-green-600 font-semibold text-xl">Loading...</div>
          </div>
        ) : (
          <>
            {data?.map((subject) => (
              <div key={subject.subject_id} className="space-y-6 mb-8">
                <h2 className="text-2xl font-extrabold text-green-700 uppercase border-b-2 border-green-300 pb-2 mb-4">
                  {subject.subject_name}
                </h2>
                {subject.questions?.map((q, index) => (
                  <div key={q.id} className="bg-white shadow-md p-6 space-y-6">
                    <h3 className="text-sm font-semibold mb-4">№ {index + 1}</h3>
                    <h2 className="text-xl font-bold inline-block uppercase">
                      {q.question_text}
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {[
                        { key: "a", text: q.version_a },
                        { key: "b", text: q.version_b },
                        { key: "c", text: q.version_c },
                        { key: "d", text: q.version_d },
                      ].map(({ key, text }) => (
                        <div key={key} className="w-auto flex items-center gap-4">
                          <p
                            className={`${
                              selectedAnswers[q.id] === key
                                ? "bg-green-500 text-white"
                                : "bg-white"
                            } shadow-md py-3 px-4 space-y-6 cursor-pointer rounded-md`}
                            onClick={() =>
                              setSelectedAnswers((prev) => ({
                                ...prev,
                                [q.id]: key,
                              }))
                            }
                          >
                            {key.toUpperCase()}
                          </p>
                          <p
                            className={`${
                              selectedAnswers[q.id] === key ? "text-green-500" : ""
                            } font-medium`}
                          >
                            {text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ))}

            <div className="flex items-center justify-center gap-4">
              <Link href="/apply/profile">
                <Button
                  variant="outline"
                  className="font-semibold cursor-pointer">
                  {t("back")}
                </Button>
              </Link>
              <button
                onClick={submitExam}
                className="btn-primary"
              >
                {t("submit")}
              </button>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default Test;
