using Application.ViewModels.Common;
using DotNetApp.ViewModels.Base;
using System;

namespace Application.ViewModels.ASIA.India.RCH
{
    public class IndiaRCHModel : BaseAppModel
    {
        public PaymentDetailsSection PaymentDetails { get; set; }
        public ChequeDetailsSection ChequeDetails { get; set; }
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
