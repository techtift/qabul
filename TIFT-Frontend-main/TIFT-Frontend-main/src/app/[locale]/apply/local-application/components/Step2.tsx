"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { ApiError, Faculty, Program, StepProps, StudyType } from "@/types";
import { getApplication } from "@/services/application.service";
import { usePathname, useRouter } from "next/navigation";
import { useTranslations } from "next-intl";
import { ApiService } from "@/services/api.service";
import { GET_STUDENT_ENDPOINT, STUDENT_APPLICATIONS_ENDPOINT } from "@/constants/api";

const Step2 = ({ setStep, data, setData }: StepProps) => {
  const t = useTranslations("LocalApplication");
  const pathname = usePathname();
  const lang = pathname.split("/")[1] || "uz";
  const localeName = `name_${lang}`;
  const router = useRouter();

  const [degree, setDegree] = useState(data.program_id?.toString() || "");
  const [files, setFiles] = useState<File[]>([]);
  const [programs, setPrograms] = useState<Program[]>([]);
  const [studyTypes, setStudyTypes] = useState<StudyType[]>([]);
  const [faculties, setFaculties] = useState<Faculty[]>([]);
  const [allFaculties, setAllFaculties] = useState<Faculty[]>([]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0]; // Get the first file
      setFiles(Array.from(e.target.files));
      setData({
        ...data,
        transcript: selectedFile,
      });
    }
  };
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0]; // Get the first file
      setFiles(Array.from(e.dataTransfer.files));
      setData({
        ...data,
        transcript: droppedFile,
      });
    }
  };
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };
  const handleClearSelection = () => {
    setFiles([]);
    setData({
      ...data,
      transcript: null,
    });
  };

  useEffect(() => {
    if (!localStorage.getItem("access_token")) {
      router.push("/");
      return;
    }
    fetchUserData();
  }, []);
  useEffect(() => {
    if (degree === "1" || degree === "29") {
      setData({
        ...data,
        is_transfer: false,
        transfer_level: null,
        transcript: null,
        program_id: parseInt(degree),
      });
    } else if (degree === "30") {
      setData({
        ...data,
        is_transfer: true,
        study_type_id: null,
        faculty_id: null,
        program_id: parseInt(degree),
      });
    }

    setFaculties(allFaculties.filter((f) => f.program_id.toString() === degree))
  }, [degree]);

  const fetchUserData = async () => {
    try {
      const res = await ApiService.get(GET_STUDENT_ENDPOINT, {});
      const resApplication = await ApiService.get(`${STUDENT_APPLICATIONS_ENDPOINT}?student_id=${res.data.id}`, {})
      if(resApplication.data.length === 0) {
        fetchApplication();
      } else if(resApplication.data[0].id) {
        router.push("/apply/profile");
      }
    } catch (error) {
      const apiError = error as ApiError;
      if(apiError.response?.data?.error_code === "not_found") {
        fetchApplication();
      }
    }
  };
  const fetchApplication = async () => {
    try {
      const res = await getApplication(lang);
      // setApplication(res);
      setData({
        ...data,
        application_id: res.id,
      });
      setPrograms(res.programs);
      setStudyTypes(res.study_types);
      setFaculties(res.faculties);
      setAllFaculties(res.faculties);
    } catch (e) {
      // console.error("Error:", e);
    }
  };
  const canContinue = () => {
    if (!degree) return false;

    if (!data.is_transfer) {
      return Boolean(data.study_type_id && data.faculty_id);
    }

    return Boolean(data.transfer_level && data.transcript);
  };

  const changeStudyType = (value: string) => {
    const selectedType = studyTypes.find((type) => type.id.toString() === value);
    if (selectedType) {
      setData({
        ...data,
        study_type_id: selectedType.id,
      });
    }
  };
  const changeFaculty = (value: string) => {
    const selectedFaculty = faculties.find((faculty) => faculty.id.toString() === value);
    if (selectedFaculty) {
      setData({
        ...data,
        faculty_id: selectedFaculty.id,
      });
    }
  };
  const changeTransferLevel = (value: string) => {
    setData({
      ...data,
      transfer_level: value,
    });
  };
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {programs && programs.length !== 0 && (
          <div className="space-y-2 col-span-1">
            <label className="block font-semibold text-sm">{t("programs")}</label>
            <Select value={degree} onValueChange={setDegree}>
              <SelectTrigger className="bg-gray-100 text-lg w-full">
                <SelectValue placeholder={t("select_program")} />
              </SelectTrigger>
              <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                {programs.map((program) => (
                  <SelectItem key={program.id} value={program.id?.toString()}>
                    {program[localeName as keyof Program]}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}
        {degree === "1" || degree === "29" ? (
          <>
            <div className="space-y-2 col-span-1">
              <label className="block font-semibold text-sm">{t("study_type")}</label>
              <Select value={data.study_type_id?.toString()} onValueChange={changeStudyType}>
                <SelectTrigger className="bg-gray-100 text-lg w-full">
                  <SelectValue placeholder={t("select_study_type")} />
                </SelectTrigger>
                <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                  {studyTypes.map((type) => (
                      degree !== "29" ? (
                        <SelectItem key={type.id} value={type.id.toString()}>
                          {type[localeName as keyof StudyType]}
                        </SelectItem>
                      ) : (
                        type.id === 1 ? (
                          <SelectItem key={type.id} value={type.id.toString()}>
                            {type[localeName as keyof StudyType]}
                          </SelectItem>
                        ) : null
                      )
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2 col-span-1">
              <label className="block font-semibold text-sm">{t("faculty")}</label>
              <Select value={data.faculty_id?.toString()} onValueChange={changeFaculty}>
                <SelectTrigger className="bg-gray-100 text-lg w-full">
                  <SelectValue placeholder={t("select_faculty")} />
                </SelectTrigger>
                <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                  {faculties?.map((faculty) => (
                    <SelectItem key={faculty.id} value={faculty.id?.toString()}>
                      {faculty[localeName as keyof Program]}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </>
        ) : (
          degree === "30" && (
            <>
              <div className="space-y-2 col-span-1">
                <label className="block font-semibold text-sm">{t("level")}</label>
                <Select value={data.transfer_level?.toString()} onValueChange={changeTransferLevel}>
                  <SelectTrigger className="bg-gray-100 text-lg w-full">
                    <SelectValue placeholder={t("select_level")} />
                  </SelectTrigger>
                  <SelectContent
                    position="popper"
                    className="w-[var(--radix-select-trigger-width)]">
                    <SelectItem value="1">1</SelectItem>
                    <SelectItem value="2">2</SelectItem>
                    <SelectItem value="3">3</SelectItem>
                    <SelectItem value="4">4</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2 col-span-2">
                <label className="block font-semibold text-sm">{t("transcript_reference")}</label>
                <div
                  className="flex flex-row items-center justify-center w-full border-2 border-dashed border-gray-300 rounded-md bg-gray-50 hover:bg-gray-100 transition-colors"
                  onDrop={handleDrop}
                  onDragOver={handleDragOver}>
                  {files.length > 0 ? (
                    <div className="p-4 text-center">
                      <ul className="mt-2 text-sm text-gray-600">
                        {files.map((file, index) => (
                          <li key={index}>{file.name}</li>
                        ))}
                      </ul>
                      <button
                        className="mt-4 text-sm text-blue-600 hover:text-blue-800"
                        onClick={handleClearSelection}>
                        {t("clear_selection")}
                      </button>
                    </div>
                  ) : (
                    <label className="flex items-center justify-between w-full h-full px-4 py-1">
                      <p className="text-gray-400">
                        <span className="font-semibold">{t("drag_and_drop")}</span>
                      </p>
                      <input
                        type="file"
                        className="hidden"
                        onChange={handleFileChange}
                        multiple={false} // Only allow single file selection
                        accept=".pdf,.doc,.docx" // Specify accepted file types if needed
                      />
                    </label>
                  )}
                </div>
              </div>
            </>
          )
        )}
      </div>

      <div className="flex flex-row gap-4 items-center justify-end pt-4">
        <Link href="/apply">
          <Button variant="outline" className="font-semibold cursor-pointer">
            {t("back")}
          </Button>
        </Link>
        <Button className="btn-primary" onClick={() => setStep(3)} disabled={!canContinue()}>
          {t("continue")}
        </Button>
      </div>
    </div>
  );
};

export default Step2;
