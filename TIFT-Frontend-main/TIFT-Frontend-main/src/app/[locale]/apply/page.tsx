"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Breadcrumb from "@/components/Breadcumb";
import { useTranslations } from "next-intl";

const Apply = () => {
  const t = useTranslations("ApplyPage");
  return (
    <>
      <Breadcrumb />
      <div className="custom-container">
        {/* Page Title */}
        <h1 className="title">
          {t("apply")}
        </h1>

        {/* Info Card */}
        <Card className="shadow-md">
          <CardContent className="px-6 md:px-8 py-2 md:py-4 space-y-8 text-start">
            <div className="space-y-2">
              <h2 className="text-2xl md:text-3xl font-bold">{t("title")}</h2>
              <p className="text-gray-600 md:max-w-4xl">{t("description")}</p>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-row gap-4">
              <Link href="/apply/local-application" className="w-full">
                <Button variant="outline" className="w-full font-semibold cursor-pointer">
                  {t("apply")}
                </Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default Apply;
