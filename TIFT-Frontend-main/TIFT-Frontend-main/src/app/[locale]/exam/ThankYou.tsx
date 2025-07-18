"use client";

import { useEffect } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { LucideCheckCircle2, LucideXCircle } from "lucide-react";
import { useTranslations } from "next-intl";

interface ThankYouProps {
  result: Record<string, unknown>;
}
const ThankYou = ({ result }: ThankYouProps) => {
  const t = useTranslations("Exam");

  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  const passed = typeof result.score_percent === "number" && result.score_percent > 30 

  return (
    <div className="text-center px-4 lg:px-28 py-20 space-y-4 bg-gradient-to-br from-green-50 via-white to-red-50 shadow-sm">
      {passed ? (
        <LucideCheckCircle2
          strokeWidth={1}
          stroke="#fff"
          fill="#22c55e"
          className="w-28 h-28 mx-auto"
        />
      ) : (
        <LucideXCircle
          strokeWidth={1}
          stroke="#fff"
          fill="#FF0000"
          className="w-28 h-28 mx-auto"
        />
      )}
      <div className="space-y-4 flex flex-col items-center">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-800">
          {t(passed ? "pass_title" : "fail_title")}
        </h2>
        <div className="text-gray-600 text-base md:text-lg space-y-1 xl:w-3xl">
          {t(passed ? "pass_description" : "fail_description")}
          <p className="font-bold">{t(passed ? "pass_welcome" : "phone_number")}</p>
        </div>
        {/* <div className="text-gray-600 text-base md:text-lg space-y-1">
          <p><strong>{t("total_questions")}:</strong> {String(result.total)} <strong className="sm:ml-2">{t("correct_answers")}:</strong> {String(result.correct)} <strong className="sm:ml-2">{t("score")}:</strong> {String(result.score_percent)}%</p>
        </div> */}

        <div className="pt-4">
          <Link href="/apply/profile">
            <Button className="btn-primary">{t("go_profile")}</Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ThankYou;
