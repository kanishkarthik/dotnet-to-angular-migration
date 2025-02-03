using Application.ViewModels.Common;
using DotNetApp.ViewModels.NAM.US.BKT;

namespace Application.ViewModels.NAM.US.BKT
{
    public class USBKTModel
    {
        public PaymentMethodModel PaymentMethod { get; set; }
        public PaymentDetailsModel PaymentDetails { get; set; }

        public BeneficiaryDetailsModel BeneficiaryDetails { get; set; }

        public OrderingPartyDetailsModel OrderingPartyDetails { get; set; }


    }
}