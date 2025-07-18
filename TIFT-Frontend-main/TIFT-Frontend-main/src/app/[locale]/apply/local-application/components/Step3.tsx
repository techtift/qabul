"use-client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { ApiError, StepProps } from "@/types";
import { toast } from "sonner";
import { createStudent, createStudentByMyGov, updateStudent } from "@/services/student.service";
import { useTranslations } from "next-intl";
import { useRouter } from "next/navigation";
import { GET_STUDENT_ENDPOINT } from "@/constants/api";
import { ApiService } from "@/services/api.service";
import { getCorrectDate } from "@/utils/date";
import { Loader } from "lucide-react";
import DatePickerWithInput from "@/components/DatePickerWithInput";

const Step3 = ({ setStep }: StepProps) => {
  const t = useTranslations("LocalApplication");
  const $t = useTranslations("Messages");
  const router = useRouter();

  const [mode, setMode] = useState<"pinfl" | "info">("pinfl")
  const [studentId, setstudentId] = useState(null)
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [fathersName, setFathersName] = useState("");
  const [citizenship, setCitizenship] = useState("");
  const [pnfl, setPnfl] = useState("");
  const [qualification, setQualification] = useState("");
  // const [gender, setGender] = useState("");
  const [birthPlace, setBirthPlace] = useState("");
  const [birthDate, setBirthDate] = useState("");
  const [schoolName, setSchoolName] = useState("");
  const [phone, setPhone] = useState("");
  const [diplomaFile, setDiplomaFile] = useState<File | null>(null);
  // const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [passportNumber, setPassportNumber] = useState("")
  const [loading, setLoading] = useState<boolean>(false)

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
  };
  const handleDiplomaChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setDiplomaFile(e.target.files[0]);
    }
  };
  const handleDiplomaDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setDiplomaFile(e.dataTransfer.files[0]);
    }
  };
  // const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  //   if (e.target.files && e.target.files.length > 0) {
  //     setPhotoFile(e.target.files[0]);
  //   }
  // };
  // const handlePhotoDrop = (e: React.DragEvent<HTMLDivElement>) => {
  //   e.preventDefault();
  //   if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
  //     setPhotoFile(e.dataTransfer.files[0]);
  //   }
  // };

  useEffect(() => {
    if (!localStorage.getItem("access_token")) {
      router.push("/");
      return;
    }
    fetchUserData();
  }, []);
  const fetchUserData = async () => {
    try {
      const res = await ApiService.get(GET_STUDENT_ENDPOINT, {});
      
      setstudentId(res.data.id);
      setFirstName(res.data.first_name || "");
      setLastName(res.data.last_name || "");
      setFathersName(res.data.father_name || "");
      setCitizenship(res.data.citizenship || "");
      setPnfl(res.data.pinfl || "");
      setPassportNumber(res.data.passport_number || "");
      setQualification(res.data.qualification?.toString() || "");
      setSchoolName(res.data.name_qualification || "");
      // setGender(res.data.gender || "");
      setBirthPlace(res.data.birth_place || "");
      setBirthDate(getCorrectDate(res.data.birth_date) || "");
      // setPhone(res.data.phone_number || "");
      setMode("info");
    } catch (error) {
      const apiError = error as ApiError;
      // if(apiError.response?.data?.error_code === "not_found") {
      //   console.log("User can fill this form");
      // }
      // console.log(apiError)
    }
  };

  const validateForm = () => {
    const isPassportValid = /^[A-Za-z]{2}\d{7}$/.test(passportNumber);
    const isValid = studentId ? (
      qualification.trim() !== "" &&
      schoolName.trim() !== "" &&
      studentId !== null
    ) : (
      firstName.trim() !== "" &&
      lastName.trim() !== "" &&
      fathersName.trim() !== "" &&
      citizenship.trim() !== "" &&
      birthPlace.trim() !== "" &&
      pnfl.trim().length === 14 &&
      isPassportValid &&
      qualification.trim() !== "" &&
      schoolName.trim() !== ""
    );
    return isValid;
  };
  const handleSubmit = async () => {
    if (!validateForm()) {
      toast($t("e_all_required"));
      return;
    }
    try {
      const formData = new FormData();

      formData.append("qualification", qualification);
      formData.append("name_qualification", schoolName);
      if(diplomaFile) formData.append("diploma", diplomaFile);
      if(phone) formData.append("additional_phone_number", phone);
      
      if (!studentId) {
        formData.append("first_name", firstName);
        formData.append("last_name", lastName);
        formData.append("father_name", fathersName);
        formData.append("birth_date", formatDateForBackend(birthDate));
        formData.append("birth_place", birthPlace);
        formData.append("citizenship", citizenship);
        formData.append("passport_number", pnfl);

        await createStudent(formData)
      } else {
        await updateStudent(formData);
      }

      setStep(4);
      toast($t("s_data_saved"));
    } catch (error) {
      if (error instanceof Error) {
        toast($t("e_unexpected_error"));
        // console.error("Error submitting form:", error);
      } else if (typeof error === "object" && error !== null && "status" in error) {
        if (error.status === 500) setStep(4);
        else {
          toast($t("e_unexpected_error"));
          // console.error("Error submitting form:", error);
        }
      }
    }
  };

  // Convert date format from DD.MM.YYYY to YYYY-MM-DD
  const formatDateForBackend = (dateString : string) => {
    if (!dateString) return '';
    
    const parts = dateString.split('.');
    if (parts.length === 3) {
      const [day, month, year] = parts;
      return `${year}-${month}-${day}`;
    }
    return dateString; // fallback if format is unexpected
  };
  const $validateForm = () => {
    const isBirthDateValid = /^\d{2}\.\d{2}\.\d{4}$/.test(birthDate);
    const isPassportValid = /^[A-Za-z]{2}\d{7}$/.test(passportNumber);
    
    const isValid = (
      birthDate.trim() !== "" &&
      passportNumber.trim() !== "" &&
      isBirthDateValid &&
      isPassportValid
    );
    
    return isValid;
  };
  const handlePINFL = async () => {
    if (!$validateForm()) {
      toast($t("e_all_required"));
      return;
    }
    try {
      setLoading(true)
      const formData = new FormData();
      formData.append("birth_date", formatDateForBackend(birthDate));
      formData.append("passport_number", passportNumber); 

      const res = await createStudentByMyGov(formData);
      // throw new Error("This function is deprecated, use createStudentByMyGov instead");

      // if(res.data.id) {
        setstudentId(res.id);
        setFirstName(res.first_name || "");
        setLastName(res.last_name || "");
        setFathersName(res.father_name || "");
        setCitizenship(res.citizenship || "");
        setPnfl(res.pinfl || "");
        setPassportNumber(res.passport_number || "");
        setQualification(res.qualification?.toString() || "");
        setSchoolName(res.name_qualification || "");
        // setGender(res.gender || ""); 
        setBirthPlace(res.birth_place || "");
        setBirthDate(getCorrectDate(res.birth_date) || "");
        // setPhone(res.phone_number || "");
        setMode("info")
      // }
      toast($t("s_data_saved"));
    } catch (error) {
      const apiError = error as ApiError;
      if (apiError.response?.data?.error_code === "not_found") {
        toast($t("e_citizen_not_found"))
      } else  if (apiError.response?.data?.error_code === "already_exists") {
        toast($t("e_already_registered"))
      } else {
        toast($t("e_my_gov"))
        setMode("info")
      }
    } finally {
      setLoading(false)
    }
  };
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mode === "pinfl" && !studentId && (
          <>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("passport_number")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("enter_passport_number")}
                value={passportNumber}
                onChange={(e) => {
                  const value = e.target.value.toUpperCase();
                  setPassportNumber(value);
                }}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
                maxLength={9}
              />
              {passportNumber && !/^[A-Za-z]{2}\d{7}$/.test(passportNumber) && (
                <p className="text-red-500 text-sm">{t("incorrect_passport_number")}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("birth_date")} <span className="text-red-500">*</span>
              </label>
              <DatePickerWithInput
                value={birthDate}
                onChange={(value) => setBirthDate(value)}
                disabled={studentId ?? false}
              />
              {birthDate && !/^\d{2}\.\d{2}\.\d{4}$/.test(birthDate) && (
                <p className="text-red-500 text-sm">{t("correct_date_format")}</p>
              )}
            </div>
          </>
        )}
        {mode === "info" && (
          <>
            <div className="space-y-2">
            <label className="block font-semibold text-sm">
              {t("first_name")} <span className="text-red-500">*</span>
            </label>
            <Input
              placeholder={t("enter_first_name")}
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="bg-gray-100 text-lg"
              disabled={studentId ?? false}
            />
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("last_name")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("enter_last_name")}
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
              />
            </div>
            <div className="space-y-2">
            <label className="block font-semibold text-sm">
              {t("father_name")} <span className="text-red-500">*</span>
            </label>
            <Input
              placeholder={t("enter_father_name")}
              value={fathersName}
              onChange={(e) => setFathersName(e.target.value)}
              className="bg-gray-100 text-lg"
              disabled={studentId ?? false}
            />
            </div>
            {/* <div className="space-y-2">
              <label className="block font-semibold text-sm">
                Gender <span className="text-red-500">*</span>
              </label>
              <Select value={gender} onValueChange={setGender}>
                <SelectTrigger className="bg-gray-100 text-lg w-full">
                  <SelectValue placeholder="Select your gender" />
                </SelectTrigger>
                <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                  <SelectItem value="male">Male</SelectItem>
                  <SelectItem value="female">Female</SelectItem>
                </SelectContent>
              </Select>
            </div> */}
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("birth_date")} <span className="text-red-500">*</span>
              </label>
              <DatePickerWithInput
                value={birthDate}
                onChange={(value) => setBirthDate(value)}
                disabled={studentId ?? false}
              />
              {birthDate && !/^\d{2}\.\d{2}\.\d{4}$/.test(birthDate) && (
                <p className="text-red-500 text-sm">{t("correct_date_format")}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("citizenship")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("select_citizenship")}
                value={citizenship}
                onChange={(e) => setCitizenship(e.target.value)}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
              />
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("birth_place")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("enter_birth_place")}
                value={birthPlace}
                onChange={(e) => setBirthPlace(e.target.value)}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
              />
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("pnfl")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("enter_pnfl")}
                value={pnfl}
                onChange={(e) => {
                  const value = e.target.value.replace(/\D/g, ''); // Remove non-digit characters
                  setPnfl(value);
                }}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
                maxLength={14}
              />
              {pnfl && !/^\d{14}$/.test(pnfl) && (
                <p className="text-red-500 text-sm">{t("incorrect_pinfl")}</p>
              )}
            </div>
            <div className="space-y-2">
              <label className="block font-semibold text-sm">
                {t("passport_number")} <span className="text-red-500">*</span>
              </label>
              <Input
                placeholder={t("enter_passport_number")}
                value={passportNumber}
                onChange={(e) => {
                  const value = e.target.value.toUpperCase();
                  setPassportNumber(value);
                }}
                className="bg-gray-100 text-lg"
                disabled={studentId ?? false}
                maxLength={9}
              />
              {passportNumber && !/^[A-Za-z]{2}\d{7}$/.test(passportNumber) && (
                <p className="text-red-500 text-sm">{t("incorrect_passport_number")}</p>
              )}
            </div>
            <div className="space-y-2 col-span-1 md:col-span-2">
              <label className="block font-semibold text-sm">{t("additional_phone_number")}</label>
              <Input
                type="tel"
                placeholder="+998 99 123 45 67"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                className="bg-gray-100 text-lg"
              />
            </div>
            <div className="space-y-2 col-span-1 md:col-span-2">
              <label className="block font-semibold text-sm">{t("qualification")}</label>
              <Select value={qualification} onValueChange={setQualification}>
                <SelectTrigger className="bg-gray-100 text-lg w-full">
                  <SelectValue placeholder={t("select_qualification")} />
                </SelectTrigger>
                <SelectContent position="popper" className="w-[var(--radix-select-trigger-width)]">
                  <SelectItem value="1">{t("middle_school")}</SelectItem>
                  <SelectItem value="2">{t("college")}</SelectItem>
                  <SelectItem value="3">{t("lyceum")}</SelectItem>
                  <SelectItem value="4">{t("university")}</SelectItem>
                  <SelectItem value="5">{t("technical_school")}</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2 col-span-1 md:col-span-2">
              <label className="block font-semibold text-sm">{t("qualification_name")}</label>
              <Input
                placeholder={t("enter_qualification_name")}
                value={schoolName}
                onChange={(e) => setSchoolName(e.target.value)}
                className="bg-gray-100 text-lg"
              />
            </div>
            {/* Diploma File Upload */}
            <div className="space-y-2 col-span-1 md:col-span-2">
              <label className="block font-semibold text-sm">{t("diplom")}</label>
              <div
                className="flex flex-row items-center justify-center w-full border-2 border-dashed border-gray-300 rounded-md bg-gray-50 hover:bg-gray-100 transition-colors"
                onDrop={handleDiplomaDrop}
                onDragOver={handleDragOver}>
                {diplomaFile ? (
                  <div className="p-4 text-center">
                    <div className="mt-2 text-sm text-gray-600">{diplomaFile.name}</div>
                    <button
                      className="mt-4 text-sm text-blue-600 hover:text-blue-800"
                      onClick={() => setDiplomaFile(null)}>
                      {t("clear_selection")}
                    </button>
                  </div>
                ) : (
                  <label className="flex items-center justify-between w-full h-full px-4 py-1 cursor-pointer">
                    <p className="text-gray-400">
                      <span className="font-semibold">{t("drag_and_drop")}</span>
                    </p>
                    <input
                      type="file"
                      className="hidden"
                      onChange={handleDiplomaChange}
                      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                    />
                  </label>
                )}
              </div>
            </div>
            {/* Photo File Upload */}
            {/* <div className="space-y-2 col-span-1 md:col-span-2">
              <label className="block font-semibold text-sm">{t("photo")}</label>
              <div
                className="flex flex-row items-center justify-center w-full border-2 border-dashed border-gray-300 rounded-md bg-gray-50 hover:bg-gray-100 transition-colors"
                onDrop={handlePhotoDrop}
                onDragOver={handleDragOver}>
                {photoFile ? (
                  <div className="p-4 text-center">
                    <div className="mt-2 text-sm text-gray-600">{photoFile.name}</div>
                    <button
                      className="mt-4 text-sm text-blue-600 hover:text-blue-800"
                      onClick={() => setPhotoFile(null)}>
                      {t("clear_selection")}
                    </button>
                  </div>
                ) : (
                  <label className="flex items-center justify-between w-full h-full px-4 py-1 cursor-pointer">
                    <p className="text-gray-400">
                      <span className="font-semibold">{t("drag_and_drop")}</span>
                    </p>
                    <input
                      type="file"
                      className="hidden"
                      onChange={handlePhotoChange}
                      accept=".jpg,.jpeg,.png"
                    />
                  </label>
                )}
              </div>
            </div> */}
          </>
        )}
      </div>

      <div className="flex flex-row gap-4 items-center justify-end pt-4">
        <Button
          onClick={() => setStep(2)}
          variant="outline"
          className="font-semibold cursor-pointer">
          {t("back")}
        </Button>
        {mode === "pinfl" ? (
          <Button className="btn-primary" onClick={handlePINFL} disabled={!$validateForm() || loading}>
            {loading && (<Loader />)} {t("continue")}
          </Button>
        ) : (
          <Button className="btn-primary" onClick={handleSubmit} disabled={!validateForm() && !studentId}>
            {t("continue")}
          </Button>
        )}
      </div>
    </div>
  );
};

export default Step3;
