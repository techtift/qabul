import { useTranslations } from "next-intl";
import Link from "next/link"; // Use next-intl's Link for localized navigation
import { Button } from "@/components/ui/button";

export default function NotFoundPage() {
  const t = useTranslations("NotFoundPage");

  return (
    <div className="flex flex-col justify-center items-center text-white py-8">
      <div className="text-center bg-white/10 backdrop-blur-md p-8 sm:p-12 rounded-xl max-w-xl w-full">
        <h1 className="text-8xl sm:text-9xl font-extrabold text-green-500 mb-4">
          {t("errorCode")}
        </h1>
        <p className="text-base sm:text-lg mb-8 text-gray-500">{t("description")}</p>
        <div className="flex items-center gap-4 justify-center">
          <Link href="/" className="btn-primary">
            {t("goHome")}
          </Link>
          <Link href="/about-us">
            <Button
              variant="outline"
              className="font-semibold cursor-pointer text-black rounded py-4 text-sm shadow px-6">
              {t("goAboutUs")}
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
}
