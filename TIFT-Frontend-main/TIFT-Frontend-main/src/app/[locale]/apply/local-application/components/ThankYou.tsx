import Link from "next/link";
import { Button } from "@/components/ui/button";
import { LucideCheckCircle2 } from "lucide-react";
import { useTranslations } from "next-intl";

const ThankYou = () => {
  const t = useTranslations("ThankYou");
  return (
    <div className="text-center px-4 lg:px-28 py-20 space-y-4 bg-gradient-to-br from-green-50 via-white to-red-50 shadow-sm">
      <LucideCheckCircle2
        strokeWidth={1}
        stroke="#fff"
        fill="#22c55e"
        className="w-28 h-28 mx-auto"
      />
      <div className="space-y-4">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-800">
          {t("title")}
        </h2>
        <div className="text-gray-500 text-sm md:text-lg">
          <p>
            {t("description")}
          </p>
        </div>

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
