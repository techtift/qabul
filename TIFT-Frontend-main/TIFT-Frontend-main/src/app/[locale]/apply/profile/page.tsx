"use client";

import { Button } from "@/components/ui/button";
import Image from "next/image";
import React, { useEffect, useState } from "react";
import Breadcrumb from "@/components/Breadcumb";
import { ApiService } from "@/services/api.service";
import { CHECK_EXAM_DATE, GET_FILE_OR_IMAGE, GET_STUDENT_ENDPOINT, STUDENT_APPLICATIONS_ENDPOINT } from "@/constants/api";
import { Download, User } from "lucide-react";
import { toast } from "sonner";
import { useRouter } from "next/navigation";
import { useTranslations, useLocale } from "next-intl";
import { getCorrectDate, getCurrentYear  } from "@/utils/date";
import { ApiError } from "@/types";
import { getCorrectPhoneNumber } from "@/utils/global";
import { getStudentContract, getStudentReference } from "@/services/student.service";

type UserData = {
  id: number;
  user_id: number;
  user_uuid: string;
  uuid: string;
  first_name: string;
  last_name: string;
  father_name: string;
  phone_number: string;
  program_name_uz: string;
  additional_phone_number: string;
  birth_date: string;
  birth_place: string;
  citizenship: string;
  pinfl: string;
  passport_number: string;
  qualification: number;
  name_qualification: string;
  diploma: string;
  photo: string;
  gender: string;
  is_attended_exam: boolean;
  is_passed_exam: boolean;
  is_exam_exempt: boolean;
};

type StudentApplication = {
  is_transfer: boolean;
  transfer_level?: string;
  program_id?: string;
  faculty_day_price?: string;
  faculty_night_price?: string;
  study_type_id?: number;
  program_name_uz?: string;
  study_type_name?: string;
  faculty_name_uz?: string;
  is_online_exam?: boolean;
  application_id?: string;
  lang?: string;
};

const Profile = () => {
  const t = useTranslations("LocalApplication");
  const $t = useTranslations("Exam");
  const _t = useTranslations("Messages");
  const router = useRouter();
  const locale = useLocale();

  const [data, setData] = useState<UserData>();
  const [studentApplication, setStudentApplication] = useState<StudentApplication | null>(null);
  const [photo, setPhoto] = useState<string | undefined>();
  const [diplomaBlobUrl, setDiplomaBlobUrl] = useState<string>("");
  const [studentId, setStudentId] = useState();
  const [loading, setLoading] = useState(false);
  const [loadingReference, setLoadingReference] = useState(false);

  const fetchUserData = async () => {
    try {
      const res = await ApiService.get(GET_STUDENT_ENDPOINT, {});
      setData(res.data);
      setStudentId(res.data.id);
      
      const resApplication = await ApiService.get(`${STUDENT_APPLICATIONS_ENDPOINT}?student_id=${res.data.id}`, {})
      setStudentApplication(resApplication.data[0]);
    } catch (error) {
      const apiError = error as ApiError;
      if(apiError.response?.data?.error_code === "not_found") {
        toast(_t("w_apply"));
        router.push("/apply/local-application");
      }
    }
  };

  useEffect(() => {
    if(localStorage.getItem("access_token")) fetchUserData();
    else router.push("/apply/local-application");
  }, []);

  const fetchImageUrl = async (photoUrl: string) => {
    try {
      const path = photoUrl.replace("http://qabul.tift.uz/media/", "");
      const response = await ApiService.getFileData(GET_FILE_OR_IMAGE, {
        params: { path },
        responseType: "blob",
      });
      const imageBlob = response.data;
      const imageObjectURL = URL.createObjectURL(imageBlob);
      setPhoto(imageObjectURL);
    } catch (error) {
      // console.error("Failed to fetch image URL:", error);
    }
  };

  useEffect(() => {
    if (data?.photo) {
      fetchImageUrl(data.photo);
    }
  }, [data?.photo]);

  const fetchDiplomaBlob = async (diplomaUrl: string) => {
    try {
      const path = diplomaUrl.replace("http://qabul.tift.uz/media/", "");
      const response = await ApiService.getFileData(GET_FILE_OR_IMAGE, {
        params: { path },
        responseType: "blob",
      });
      const blobUrl = URL.createObjectURL(response.data);
      setDiplomaBlobUrl(blobUrl);
    } catch (error) {
      // console.error("Failed to fetch diploma file:", error);
    }
  };

  useEffect(() => {
    if (data?.diploma) {
      fetchDiplomaBlob(data.diploma);
    }
  }, [data?.diploma]);

  const checkExamDate = async () => {
    try {
      const response = await ApiService.post(`${CHECK_EXAM_DATE}?student_id=${studentId}`, {});
      if (response?.data?.is_valid) {
        router.push("/exam");
      } else {
        toast.error("Sizning imtihon sanangiz hali kelmagan yoki o'tkazib yuborilgan.");
      }
    } catch (error) {
      // console.error("Failed to check exam date:", error);
    }
  }
  const handleDownload = async () => {
    if (!data?.id) return;
    try {
      setLoading(true);
      const response = await getStudentContract(data.id, locale);

      // Create blob URL
      const blob = new Blob([response], { type: 'application/pdf' });
      const blobUrl = URL.createObjectURL(blob);

      // Create a temporary anchor element
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `contract-${data.id}.pdf`; // Set a filename
      a.style.display = 'none';

      // Append to body and trigger click
      document.body.appendChild(a);
      a.click();

      // Cleanup
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(blobUrl);
      }, 1000);

    } catch (error) {
      console.error('Error downloading contract:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadReference = async () => {
    if (!data?.id) return;
    try {
      setLoadingReference(true);
      const response = await getStudentReference(data.id, locale);

      // Create blob URL
      const blob = new Blob([response], { type: 'application/pdf' });
      const blobUrl = URL.createObjectURL(blob);

      // Create a temporary anchor element
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `contract-${data.id}.pdf`; // Set a filename
      a.style.display = 'none';

      // Append to body and trigger click
      document.body.appendChild(a);
      a.click();

      // Cleanup
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(blobUrl);
      }, 1000);

    } catch (error) {
      console.error('Error downloading contract:', error);
    } finally {
      setLoadingReference(false);
    }
  };

  return (
    <>
      <Breadcrumb />
      <div className="custom-container">
        <h1 className="title">
          {t("title")}
        </h1>

        <div className="flex flex-col sm:flex-row items-center gap-0">
          <div className="w-60 h-72 overflow-hidden shadow-md">
            {photo ? (
              <Image
                src={photo}
                alt={`${data?.first_name} ${data?.last_name}`}
                className="w-full h-full"
                width={60}
                height={60}
              />
            ) : (
              <User className="w-full h-full" />
            )}
          </div>
          <div className="bg-white px-6 py-10 space-y-4 flex-1">
            <h2 className="text-2xl font-bold border-b-4 border-green-600 inline-block uppercase">
              {data?.first_name} {data?.last_name} {data?.father_name}
            </h2>
            <p className="text-green-500 text-lg">
              {data?.is_attended_exam ? t("student") : "Abiturent"} • ID {`${getCurrentYear() ?? ""}_${data?.pinfl ?? ""}`}
            </p>

            {data && data?.is_attended_exam && data?.is_passed_exam && (
              <div className="flex flex-col sm:flex-row items-center gap-4">
                <Button className="btn-primary" onClick={handleDownload} disabled={loading}>
                  <Download className="mr-2 h-4 w-4" />
                  {loading ? 'Loading...' : t("download_contract")}
                </Button>
                <Button className="btn-primary" onClick={handleDownloadReference} disabled={loadingReference}>
                  <Download className="mr-2 h-4 w-4" />
                  {loadingReference ? 'Loading...' : t("download_reference")}
                </Button>
              </div>
            )}
            
            {data && data?.is_attended_exam && !data?.is_passed_exam && !data?.is_exam_exempt && (
              <p className="text-red-500 text-md">
                {$t("fail_description")} {$t("phone_number")}
              </p>
            )}
          </div>
        </div>

        <div className="bg-white shadow-md p-6 space-y-6">
          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">
              {t("personal_info")}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">{t("phone_number")}</p>
                <p className="font-medium">
                  {data?.phone_number
                    ? getCorrectPhoneNumber(data?.phone_number)
                    : "-"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("passport_number")}</p>
                <p className="font-medium">{data?.passport_number}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("birth_date")}</p>
                <p className="font-medium">{getCorrectDate(data?.birth_date ?? "")}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t-2 border-gray-200">
              <div>
                <p className="text-sm text-gray-500">{t("full_name")}</p>
                <p className="font-medium">
                  {data?.first_name} {data?.last_name} {data?.father_name}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("pnfl")}</p>
                <p className="font-medium">{data?.pinfl}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("gender")}</p>
                <p className="font-medium">{data?.gender == "1" ? t("male") : t("female") }</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t-2 border-gray-200">
              <div>
                <p className="text-sm text-gray-500">{t("citizenship")}</p>
                <p className="font-medium uppercase">{data?.citizenship}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("additional_phone_number")}</p>
                <p className="font-medium">
                  {data?.additional_phone_number
                    ? getCorrectPhoneNumber(data.additional_phone_number)
                    : "-"}
                </p>
              </div>
              <div></div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold pt-4 border-t-2 border-gray-200">
              {t("education_background")}
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">{t("qualification")}</p>
                <p className="font-medium">{data?.name_qualification}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("qualification_name")}</p>
                <p className="font-medium">
                  {data?.qualification === 1
                    ? "Middle School"
                    : data?.qualification === 2
                    ? "College"
                    : data?.qualification === 3
                    ? "Lyceum"
                    : data?.qualification === 4
                    ? "University"
                    : data?.qualification === 5
                    ? "Technical School"
                    : "-"}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500">{t("diplom")}</p>
                {diplomaBlobUrl ? (
                  <a
                    href={diplomaBlobUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium text-blue-600 hover:underline cursor-pointer"
                  >
                    {t("download_diploma")}
                  </a>
                ) : (
                  <p className="font-medium text-gray-400">
                    {t("no_diploma")}
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="space-y-4">
            <h3 className="text-xl font-semibold border-t-2 border-gray-200 pt-2">
              {t("education_programs")}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-gray-500">{t("programs")}</p>
                <p className="font-medium">{studentApplication?.program_name_uz}</p>
              </div>
              {!studentApplication?.is_transfer ? (
                <>
                  <div>
                    <p className="text-sm text-gray-500">{t("study_type")}</p>
                    <p className="font-medium">{studentApplication?.study_type_name}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">{t("faculty")}</p>
                    <p className="font-medium">{studentApplication?.faculty_name_uz}</p>
                  </div>
                </>
              ) : (
                  <div>
                    <p className="text-sm text-gray-500">{t("level")}</p>
                    <p className="font-medium">{ studentApplication?.transfer_level }</p>
                  </div>
              )}
            </div>

            <div className="grid grid-cols-1 gap-4 py-2 border-t-2 border-gray-200">
              <div>
                <p className="text-sm text-gray-500">{t("exam_form")}</p>
                <p className="font-medium">{studentApplication?.is_online_exam ? "Online" : "Offline"}</p>
              </div>
            </div>
          </div>

          {data && studentApplication && !data?.is_attended_exam && (
            <div className="flex flex-col md:flex-row items-center justify-between bg-gray-100 p-4 rounded-lg">
              <div>
                <h3 className="text-lg font-semibold mb-2">
                  {t("exam_form")}: {studentApplication?.is_online_exam ? "Online" : "Offline"}
                </h3>
                <p className="mb-4 text-center">ID {`${getCurrentYear() ?? ""}_${data?.pinfl ?? ""}`}</p>
              </div>
              <Button className="btn-primary" onClick={checkExamDate}>{t("start_exam")}</Button>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Profile;