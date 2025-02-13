using Application.ViewModels.Common;
using System;

namespace Application.ViewModels.ASIA.India.RCH
{
    public class IndiaRCHModel
    {
        public PaymentMethodSection PaymentMethod { get; set; }
        public PaymentDetailsSection PaymentDetails { get; set; }
        public ChequeDetailsSection ChequeDetails { get; set; }
    }

    public class PaymentMethodSection
    {
        public string AccountNumber { get; set; }
        public string PaymentCurrency { get; set; }
        public decimal Amount { get; set; }
        public string AccountName { get; set; }
        public string PaymentMethod { get; set; }
    }

    public class PaymentDetailsSection
    {
        public string TranRefNo { get; set; }
        public DateTime ValueDate { get; set; }
        public string PurposeCode { get; set; }
        public string PurposeDescription { get; set; }
        public string RemittanceInfo { get; set; }
    }

    public class ChequeDetailsSection
    {
        public string ChequeNumber { get; set; }
        public string PayeeName { get; set; }
        public DateTime ChequeDate { get; set; }
        public string ChequeType { get; set; }
        public string DeliveryMethod { get; set; }
        public string DeliveryAddress { get; set; }
        public string ContactNumber { get; set; }
        public string SpecialInstructions { get; set; }
    }
}
