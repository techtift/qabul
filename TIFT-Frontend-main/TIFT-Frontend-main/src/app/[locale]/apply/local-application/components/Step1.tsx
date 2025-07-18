"use client";

import { Button } from "@/components/ui/button";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import InputPhoneNumber from "@/components/InputPhoneNumber";
import { ApiService } from "@/services/api.service";
import { toast } from "sonner";
import { OTP_RESEND_TIMEOUT } from "@/constants/timers";
import { CREATE_OTP_ENDPOINT, CREATE_USER_ENDPOINT, GET_STUDENT_ENDPOINT, LOGIN_ENDPOINT, STUDENT_APPLICATIONS_ENDPOINT, USER_ME_ENDPOINT } from "@/constants/api";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { ApiError, StepProps } from "@/types";
import { useTranslations } from "next-intl";
import { useRouter, useSearchParams } from "next/navigation";
import { getMaskedPhone, formatTime } from "@/utils/global";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSeparator,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import { confirmResetPassword, requestResetPassword, verifyResetPassword } from "@/services/user.service";

export default function Step1({ setStep }: StepProps) {
  const t = useTranslations("LocalApplication");
  const $t = useTranslations("Messages");
  const router = useRouter();
  const otpRef = useRef<HTMLInputElement>(null);
  const nextBtnRef = useRef<HTMLButtonElement>(null);

  const [mode, setMode] = useState<"phone" | "verify" | "register" | "login" | "reset" | "new_password">("phone");
  const [phone, setPhone] = useState("+998");
  useEffect(() => {
    const savedPhone = localStorage.getItem("phone");
    const token = localStorage.getItem("access_token");
    if (savedPhone) {
      setPhone(savedPhone);
      setMode("register")
    }
    if (token){
      setStep(2)
    }
  }, []);

  const searchParams = useSearchParams();
  const source = searchParams.get('source') || "";

  useEffect(() => {
    const sourceParam = searchParams.get("source");
    if (sourceParam) {
      localStorage.setItem("qr_source", sourceParam);
    }
  }, []);

  const [code, setCode] = useState("");
  const [timer, setTimer] = useState(OTP_RESEND_TIMEOUT);
  const [isResendDisabled, setIsResendDisabled] = useState(true);
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  useEffect(() => {
    if(phone && phone.length === 17) nextBtnRef.current?.focus();
  }, [phone]);

  useEffect(() => {
    if (mode === "verify" || mode === "reset") {
      focusOTP();
      if (timer > 0) {
        setIsResendDisabled(true);
        const interval = setInterval(() => setTimer((t) => t - 1), 1000);
        return () => clearInterval(interval);
      } else {
        setIsResendDisabled(false);
      }
    }
  }, [mode, timer]);
  useEffect(() => {
    if (mode !== 'verify' && mode !== 'reset') return;
    focusOTP();
    if ('OTPCredential' in window && window.isSecureContext) {
      const abortController = new AbortController();

      queueMicrotask(() => {
        navigator.credentials
          .get({
            otp: { transport: ['sms'] },
            signal: abortController.signal,
          })
          .then((otp) => {
            if (otp && typeof otp === 'object' && 'code' in otp) {
              const code = (otp as { code: string }).code;
              setCode(code);
              if (code.length === 6) {
                submitOTP();
              }
            }
          })
          .catch((err) => {
            // console.log('OTP retrieval cancelled or failed:', err);
          });
      });

      return () => {
        abortController.abort();
      };
    }
  }, [mode]);

  const focusOTP = () => {
    if (otpRef.current) {     
      setTimeout(() => {
        otpRef.current?.focus();
      }, 100);
    }
  }
  const checkNumber = async () => {
    try {
      await ApiService.post(LOGIN_ENDPOINT, {
        phone_number: phone.split(" ").join(""),
        password: "_",
      });
    } catch (error) {
      const apiError = error as ApiError;
      return apiError.response?.data?.error_code || "unknown_error";
    }
  }
  const handleContinue = async () => {
    if (phone.length !== 17) {
      return;
    }
    
    const error = await checkNumber();
    if (error === "incorrect_password") {
      setMode("login")
      return;
    }

    try {
      const data = {
        phone_number: phone.split(" ").join(""),
      };
      const res = await ApiService.post(CREATE_OTP_ENDPOINT, data);

      const isSent = res?.data?.is_sent;
      if (isSent) {
        toast($t("s_sms_sent"));
        setMode("verify");
        setTimer(OTP_RESEND_TIMEOUT);
        setIsResendDisabled(true);
        focusOTP();
      }
    } catch (error) {
      const msg = $t("e_sms_sent");
      toast(msg);
      // console.error("Error:", error);
    }
  };
  const handleResendOTP = async () => {
    if (isResendDisabled) return;

    try {
      const data = {
        phone_number: phone.split(" ").join(""),
      };
      const res = await ApiService.post(CREATE_OTP_ENDPOINT, data);

      const isSent = res?.data?.is_sent;
      if (isSent) {
        toast($t("s_sms_sent"));
        setTimer(OTP_RESEND_TIMEOUT);
        setIsResendDisabled(true);
        focusOTP();
      }
    } catch (error) {
      toast($t("e_sms_sent"));
      // console.error("Error:", error);
    }
  };

  const submitOTP = async () => {
    if (code.length < 6) {
      toast($t("e_invalid_code"));
      return;
    }
    try {
      const data = {
        phone_number: phone.split(" ").join(""),
        code: code,
      };
      const res = await ApiService.post(CREATE_OTP_ENDPOINT, data);
      if (res.data?.is_verified) {
        toast($t("s_phone_verified"));
        setMode("register");
        localStorage.setItem("phone", phone.split(" ").join(""));
      }
    } catch (error) {
      // console.error("Error:", error);
      if (axios.isAxiosError(error)) {
        const errorCode = error.response?.data?.error_code;

        if (errorCode === "expired_otp") {
          toast($t("e_expired_otp"));
        } else if (errorCode === "invalid_input") {
          toast($t("e_invalid_code"));
        } else {
          toast($t("e_unexpected_error"));
        }
      } else {
        toast($t("e_unexpected_error"));
      }
    }
  };

  const checkApplicationStatus = async (studentId : string) => {
    try {
      const resApplication = await ApiService.get(`${STUDENT_APPLICATIONS_ENDPOINT}?student_id=${studentId}`, {})
      if (resApplication.data.length === 0) {
        setStep(2);
      } else if(resApplication.data[0].id) {
        router.push("/apply/profile");
      }
    } catch (error) {
      const apiError = error as ApiError;
      if(apiError.response?.data?.error_code === "not_found") {
        setStep(2);
      }
    }
  }
  const handleNextStep = async () => {
    try {
      const res = await ApiService.get(GET_STUDENT_ENDPOINT, {});
      if(res.data && res.data.id) checkApplicationStatus(res?.data?.id)
    } catch (error) {
      const apiError = error as ApiError;
      if(apiError.response?.data?.error_code === "not_found") {
        setStep(2);
      }
    }
  }
  const register = async () => {
    if (password && password.length < 6) {
      toast($t("e_password_length"));
      return;
    }
    if (!password || !confirmPassword || password !== confirmPassword) {
      toast($t("e_password_mismatch"));
      return;
    }
    try {
      const data: { phone_number: string; password: string; source?: string } = {
        phone_number: localStorage.getItem("phone") || phone.split(" ").join(""),
        password: password,
      };
      if (source.length > 0) {
        data.source = source;
      }
      const res = await ApiService.post(CREATE_USER_ENDPOINT, data);
      localStorage.setItem("access_token", res.data?.access_token);
      localStorage.setItem("refresh_token", res.data?.refresh_token);
      toast($t("s_registered"))
      handleNextStep();
    } catch (error) {
      const apiError = error as ApiError;
      const token = localStorage.getItem("access_token");
      if(apiError.response?.data?.error_code === "already_exists" && !token) {
        setMode("login");
        toast($t("w_account_exists"));
      } else if(apiError.response?.data?.error_code === "already_exists" && token) {
        toast($t("s_login"));
        setStep(2);
      } else {
        toast($t("e_unexpected_error"));
      }
    }
  };
  const login = async () => {
    if (!phone || !password) {
      toast($t("e_all_required"));
      return;
    }
    try {
      const res = await ApiService.post(LOGIN_ENDPOINT, {
        phone_number: phone.split(" ").join(""),
        password,
      });
      localStorage.setItem("access_token", res.data?.access_token);
      localStorage.setItem("refresh_token", res.data?.refresh_token);
      if (res.data?.access_token) fetchUserDetails();
      toast($t("s_login"));
      handleNextStep();
    } catch (error) {
      // console.error("Login error:", error);
      toast($t("e_invalid_login_credentials"));
    }
  };
  const fetchUserDetails = async () => {
    try {
      const res = await ApiService.get(USER_ME_ENDPOINT, {});
      localStorage.setItem("user", JSON.stringify(res.data));
    } catch (error) {
      // console.error("Failed to fetch user details:", error);
    }
  };

  const resetPassword = async () => {
    if (phone.length !== 17) return;
    try {
      await requestResetPassword({phone_number: phone.split(" ").join("")})
      toast($t("s_reset_psw_request"))
      setMode("reset")
    } catch (error) {
      // console.log(error);
      toast($t("e_reset_psw_request"))
    }
  }
  const resendOTP4Reset = async () => {
    if (isResendDisabled) return;
    try {
      await requestResetPassword({phone_number: phone.split(" ").join("")})

      toast($t("s_sms_sent"));
      setTimer(OTP_RESEND_TIMEOUT);
      setIsResendDisabled(true);
      focusOTP();
    } catch (error) {
      toast($t("e_sms_sent"));
      // console.error("Error:", error);
    }
  };
  const verifyCode = async () => {
    if (code.length !== 6) return;
    try {
      await verifyResetPassword({ phone_number: phone.split(" ").join(""), code })

      toast($t("s_phone_verified"));
      localStorage.setItem("phone", phone.split(" ").join(""));
      setMode("new_password")
    } catch (error) {
      // console.error("Error:", error);
      const apiError = error as ApiError
      const errorCode = apiError.response?.data?.error_code;

      if (errorCode === "expired_otp") {
        toast($t("e_expired_otp"));
      } else if (errorCode === "invalid_input") {
        toast($t("e_invalid_code"));
      } else {
        toast($t("e_unexpected_error"));
      }
    }
  };
  const saveNewPassword = async () => {
    if (password && password.length < 6) {
      toast($t("e_password_length"));
      return;
    }
    if (!password || !confirmPassword || password !== confirmPassword) {
      toast($t("e_password_mismatch"));
      return;
    }
    try {
      await confirmResetPassword({ 
        phone_number: phone.split(" ").join(""), new_password: password 
      });

      toast($t("s_data_saved"));
      login();
    } catch (error) {
      const apiError = error as ApiError;
      // console.log(apiError)
      toast($t("e_unexpected_error"));
    }
  };
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-4">
        {mode === "phone" ? (
          <div className="space-y-2 col-span-1">
            <InputPhoneNumber phone={phone} setPhone={setPhone} />
          </div>
        ) : (
          <>
            <div className="space-y-4 col-span-1">
              <p className="text-lg font-semibold px-2 py-1 rounded bg-gray-100 inline-block">
                {getMaskedPhone(phone)}
              </p>

              {mode === "verify" || mode === "reset" ? (
                <>
                  <div className="flex justify-center">
                    <InputOTP type="text"  autoComplete="one-time-code" inputMode="numeric" ref={otpRef} maxLength={6} value={code} onChange={setCode} autoFocus>
                      <InputOTPGroup>
                        <InputOTPSlot inputMode="numeric" index={0} />
                        <InputOTPSlot inputMode="numeric" index={1} />
                        <InputOTPSlot inputMode="numeric" index={2} />
                      </InputOTPGroup>
                      <InputOTPSeparator />
                      <InputOTPGroup>
                        <InputOTPSlot inputMode="numeric" index={3} />
                        <InputOTPSlot inputMode="numeric" index={4} />
                        <InputOTPSlot inputMode="numeric" index={5} />
                      </InputOTPGroup>
                    </InputOTP>
                  </div>
                  <p className="text-sm text-muted-foreground text-center">
                    {isResendDisabled ? (
                      <>
                        {t("send_after")}:{" "}
                        <span className="font-semibold">{formatTime(timer)}</span>
                      </>
                    ) : (
                      <button
                        onClick={mode === "reset" ? resendOTP4Reset : handleResendOTP}
                        className="font-semibold text-primary hover:underline cursor-pointer">
                        {t("send_again")}
                      </button>
                    )}
                  </p>
                </>
              ) : (
                <>
                  <div className="space-y-2">
                    <label className="block font-semibold text-sm" htmlFor="password">
                      {t(mode === "register" || mode === "new_password" ? "new_password" : "password")}
                    </label>
                    <Input
                      id="password"
                      type="password"
                      autoComplete="new-password"
                      placeholder={t(mode === "register" || mode === "new_password" ? "enter_new_password" : "enter_password")}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className={`bg-gray-100 text-lg w-full ${
                        password && password.length < 6 ? "border-red-500" : ""
                      }`}
                    />
                  </div>
                  {mode === "register" || mode === "new_password" ? (<div className="space-y-2">
                    <label className="block font-semibold text-sm" htmlFor="confirm-password">
                      {t("confirm_password")}
                    </label>
                    <Input
                      id="confirm-password"
                      type="password"
                      autoComplete="new-password"
                      placeholder={t("enter_confirm_password")}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      className={`bg-gray-100 text-lg w-full ${
                        confirmPassword && password && password !== confirmPassword
                          ? "border-red-500"
                          : ""
                      }`}
                      disabled={!password}
                    />
                  </div>) : (
                    <button
                      onClick={resetPassword}
                      className="text-xs font-semibold text-green-600 hover:underline cursor-pointer flex items-center gap-1">
                      {t("reset_password")}
                    </button>
                  )}
                </>
              )}
            </div>
          </>
        )}
      </div>

      <div className="flex flex-row gap-4 items-center justify-end pt-4">
        {mode === "phone" ? (
          <>
            <Link href="/apply">
              <Button variant="outline" className="font-semibold cursor-pointer">
                {t("back")}
              </Button>
            </Link>
            <Button
              ref={nextBtnRef}
              className="btn-primary"
              onClick={handleContinue}
              disabled={phone.split(" ").join("").length !== 13}>
              {t("continue")}
            </Button>
          </>
        ) : mode === "verify" || mode === "reset" ? (
          <>
            <Button
              variant="outline"
              className="font-semibold cursor-pointer"
              onClick={() => {
                setMode("phone")
                setCode("");
              }}>
              {t("back")}
            </Button>
            <Button className="btn-primary" onClick={mode === "reset" ? verifyCode : submitOTP} disabled={code.length < 6}>
              {t("confirm")}
            </Button>
          </>
        ) : mode === "register" || mode === "new_password" ? (
          <>
            <Button
              variant="outline"
              className="font-semibold cursor-pointer"
              onClick={() => {
                localStorage.removeItem("phone");
                setPhone("+998");
                setMode("phone");
              }}>
              {t("back")}
            </Button>
            <Button
              className="btn-primary"
              onClick={mode === "register" ? register : saveNewPassword}
              disabled={!password || !confirmPassword || password !== confirmPassword}>
              {t(mode === "register" ? "register" : "continue")}
            </Button>
          </>
        ) : mode === "login" && (
          <>
            <Button
              variant="outline"
              className="font-semibold cursor-pointer"
              onClick={() => {
                localStorage.removeItem("phone");
                setPhone("+998");
                setMode("phone");
              }}>
              {t("back")}
            </Button>
            <Button
              className="btn-primary"
              onClick={login}
              disabled={!password}>
              {t("login")}
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
