"use client";

import { Link } from "@/i18n/navigation";
import { Button } from "@/components/ui/button";
import { useTranslations } from "next-intl";
import Image from "next/image";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useState, useEffect } from "react";

export default function Home() {
  const t = useTranslations("HomePage");
  const [currentSlide, setCurrentSlide] = useState(0);
  const images = [1, 2, 3, 4, 5, 6];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % images.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + images.length) % images.length);
  };

  const goToSlide = (index: number) => {
    setCurrentSlide(index);
  };

  useEffect(() => {
    // Set up the timer for automatic slide change
    const timer = setInterval(() => {
      nextSlide();
    }, 3000); // 3000 milliseconds = 3 seconds

    // Clear the timer when the component unmounts or when currentSlide changes
    return () => clearInterval(timer);
  }, [currentSlide]); // Add currentSlide to dependencies to reset timer when slide changes

  return (
    <>
      <main className="relative w-full h-screen">
        <div className="relative w-full h-full">
          <div className="relative h-full overflow-hidden">
            {images.map((num, idx) => (
              <div
                key={num}
                className={`absolute inset-0 duration-700 ease-in-out ${idx === currentSlide ? "block" : "hidden"}`}
              >
                <Image
                  src={`/img-${num}.JPG`}
                  alt={`Carousel image ${num}`}
                  fill
                  sizes="100vw"
                  className="object-cover"
                  quality={80}
                  priority={idx === 0}
                />
                <div className="absolute inset-0 bg-black/40"></div>
              </div>
            ))}
          </div>

          <div className="absolute z-30 flex -translate-x-1/2 bottom-5 left-1/2 space-x-3 rtl:space-x-reverse">
            {images.map((_, index) => (
              <button
                key={index}
                type="button"
                className={`w-3 h-3 rounded-full ${currentSlide === index ? "bg-white" : "bg-white/50 hover:bg-white"}`}
                onClick={() => goToSlide(index)}
              />
            ))}
          </div>

          <button
            type="button"
            className="absolute top-0 left-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
            onClick={prevSlide}
          >
            <span className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white/30 group-hover:bg-white/50">
              <ChevronLeft className="text-white w-5 h-5" />
            </span>
          </button>
          <button
            type="button"
            className="absolute top-0 right-0 z-30 flex items-center justify-center h-full px-4 cursor-pointer group focus:outline-none"
            onClick={nextSlide}
          >
            <span className="inline-flex items-center justify-center w-10 h-10 rounded-full bg-white/30 group-hover:bg-white/50">
              <ChevronRight className="text-white w-5 h-5" />
            </span>
          </button>
        </div>

        <div className="absolute inset-x-0 bottom-40 sm:bottom-20 flex flex-col items-center justify-center gap-10 p-24 z-20 text-white">
          <h1 className="text-xl sm:text-4xl font-bold text-center">{t("title")}</h1>
          <Link href="/apply">
            <Button variant="default" className="btn-primary">
              {t("apply")}
            </Button>
          </Link>
        </div>
      </main>
    </>
  );
}