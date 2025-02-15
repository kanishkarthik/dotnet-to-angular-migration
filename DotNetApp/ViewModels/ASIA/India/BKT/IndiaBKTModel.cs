using Application.ViewModels.Common;
using DotNetApp.ViewModels.Base;
using DotNetApp.ViewModels.NAM.US.BKT;

namespace Application.ViewModels.ASIA.India.BKT
{
    public class IndiaBKTModel : BaseAppModel
    {        
        public PaymentDetailsModel PaymentDetails { get; set; }

        public BeneficiaryDetailsModel BeneficiaryDetails { get; set; }

        public OrderingPartyDetailsModel OrderingPartyDetails { get; set; }

    }
}