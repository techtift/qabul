"use client";

import { Button } from "@/components/ui/button";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { useEffect, useState } from "react";
import { TriangleAlert } from "lucide-react";
import { StepProps } from "@/types";
import { useTranslations } from "next-intl";
import { createApplication, createStudentDTM } from "@/services/application.service";
import { toast } from "sonner";
import { getUserMe } from "@/services/user.service";

const Step4 = ({ setStep, data, setData }: StepProps) => {
  const t = useTranslations("LocalApplication");

  const [examForm, setExamForm] = useState("");
  const [examLanguage, setExamLanguage] = useState("");
  const [dateOfExam, setDateOfExam] = useState("");
  const [files, setFiles] = useState<File[]>([]);

  useEffect(() => {
    if (examForm) {
      setData({
        ...data,
        is_online_exam: examForm === "online" || examForm === "preferential",
      });
    }
  }, [examForm]);

  const getMyId = async () => {
    try {
      const res = await getUserMe();
      return res.id || null;
    } catch (error) {
      // console.error("Error fetching user ID:", error);
    }
  };
  const createStudentApplication = async () => {
    try {
      const formData = new FormData();

      formData.append("application_id", data.application_id?.toString() ?? "");
      formData.append("program_id", data.program_id?.toString() ?? "");
      formData.append("faculty_id", data.faculty_id?.toString() ?? "");
      formData.append("is_transfer", data.is_transfer.toString());
      formData.append(
        "user_id",
        data.user_id
          ? data.user_id?.toString()
          : localStorage.getItem("user")
          ? JSON.parse(localStorage.getItem("user") || "{}").id
          : getMyId() ?? ""
      );
      formData.append("study_type_id", data.study_type_id?.toString() ?? "");
      formData.append("is_online_exam", data.is_online_exam.toString());
      formData.append("exam_date_id", data.exam_date_id?.toString() ?? "");
      formData.append("transfer_level", data.transfer_level ?? "");
      formData.append("lang", examLanguage ?? "uz");
      if (data.transcript) formData.append("transcript", data.transcript ?? "");

      await createApplication(formData);

      if (files[0]) {
        const formDataStudentDTM = new FormData()
        
        formDataStudentDTM.append("dtm_file", files[0]);
        await createStudentDTM(formDataStudentDTM)
      }

      toast("Hujjatlaringiz muvaffaqiyatli yuborildi!");
      setStep(5);
    } catch (e) {
      // console.error("Error:", e);
    }
  };

  // useEffect(() => {
  //   if (!localStorage.getItem("access_token")) {
  //     window.location.href = "/apply";
  //     return;
  //   }
  //   fetchApplication();
  // }, []);

  // const fetchApplication = async () => {
  //   try {
  //     const res = await getApplication("uz");

  //     console.log("Application Data:", res);
  //   } catch (e) {
      // console.error("Error:", e);
  //   }
  // };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(Array.from(e.dataTransfer.files)); // hammasini qo‘shish
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFiles(Array.from(e.target.files)); // fayllarni massivga aylantirib qo'shish
    }
  };
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="space-y-2 col-span-1">
          <label className="block font-semibold text-sm">{t("exam_form")}</label>
          <Select value={examForm} onValueChange={setExamForm}>
            <SelectTrigger className="bg-gray-100 text-lg w-full">
              <SelectValue placeholder={t("select_exam_form")} />
            </SelectTrigger>
            <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
              {/* <SelectItem value="offline">{t("offline")}</SelectItem> */}
              <SelectItem value="online">{t("online")}</SelectItem>
              <SelectItem value="preferential">{t("preferential")}</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2 col-span-1">
          <label className="block font-semibold text-sm">{t("exam_language")}</label>
          <Select value={examLanguage} onValueChange={setExamLanguage}>
            <SelectTrigger className="bg-gray-100 text-lg w-full">
              <SelectValue placeholder={t("select_exam_language")} />
            </SelectTrigger>
            <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
              <SelectItem value="uz">{t("uzbek")}</SelectItem>
              <SelectItem value="ru">{t("russian")}</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {examForm === "offline" ? (
          <div className="space-y-2 col-span-1">
            <label className="block font-semibold text-sm">{t("exam_date")}</label>
            <Select value={dateOfExam} onValueChange={setDateOfExam}>
              <SelectTrigger className="bg-gray-100 text-lg w-full">
                <SelectValue placeholder={t("select_exam_date")} />
              </SelectTrigger>
              <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                <SelectItem value="1">Waiting for Response from backend...</SelectItem>
                <SelectItem value="2">Waiting for Response from backend...</SelectItem>
                <SelectItem value="3">Waiting for Response from backend...</SelectItem>
              </SelectContent>
            </Select>
          </div>
        ) : examForm === "preferential" ? (
            <>
              {/* <div className="space-y-2 col-span-1">
                <label className="block font-semibold text-sm">Reason</label>
                <Select value={reason} onValueChange={setReason}>
                  <SelectTrigger className="bg-gray-100 text-lg w-full">
                    <SelectValue placeholder="Select type of reason" />
                  </SelectTrigger>
                  <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                    <SelectItem value="bachelor">waiting for backend...</SelectItem>
                    <SelectItem value="masters">waiting for backend...</SelectItem>
                    <SelectItem value="transfer">waiting for backend...</SelectItem>
                  </SelectContent>
                </Select>
              </div> */}
              {/* Diploma Upload */}
              <div className="space-y-2 col-span-1 md:col-span-2">
                <label className="block font-semibold text-sm">{t("reasonFile")}</label>
                <div
                  className="flex flex-row items-center justify-center w-full border-2 border-dashed border-gray-300 rounded-md bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}>
                  {files.length > 0 ? (
                    <div className="p-4 text-center">
                      <p className="font-medium">{files.length} file(s) selected</p>
                      <ul className="mt-2 text-sm text-gray-600">
                        {files.map((file, index) => (
                          <li key={index}>{file.name}</li>
                        ))}
                      </ul>
                      <button
                        className="mt-4 text-sm text-blue-600 hover:text-blue-800"
                        onClick={() => setFiles([])}
                        >
                        Clear selection
                      </button>
                    </div>
                  ) : (
                    <label className="flex items-center justify-between w-full h-full cursor-pointer px-4 py-1">
                      <p className="text-gray-400">
                        <span className="font-semibold">
                          {t("drag_and_drop")}
                        </span>
                      </p>
                      <input
                        type="file"
                        className="hidden"
                        onChange={handleFileChange}
                        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                      />
                    </label>
                  )}
                </div>
              </div>
            </>) : examForm === "online" && (
            <div className="space-y-2 col-span-1">
              <div className="bg-gray-100 flex flex-row items-center gap-4 p-4 rounded-md">
                <TriangleAlert className="h-10 w-10 text-yellow-500" />
                <p className="font-semibold md:text-lg">{t("online_exam_alert")}</p>
              </div>
            </div>
          
        )}
      </div>

      <div className="flex flex-row gap-4 items-center justify-end pt-4">
        <Button
          onClick={() => setStep(3)}
          variant="outline"
          className="font-semibold cursor-pointer">
          {t("back")}
        </Button>
        <Button className="btn-primary" onClick={createStudentApplication}
          disabled={
            !examForm ||
            !examLanguage ||
            (examForm === "preferential" && files.length === 0)
          }>
          {t("continue")}
        </Button>
      </div>
    </div>
  );
};

export default Step4;
