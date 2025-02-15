using DotNetApp.ViewModels.Base;

namespace Application.ViewModels.ASIA.India.BKT
{
    public class IndiaBKTModel : BaseAppModel
    {        
        public PaymentDetailsModel PaymentDetails { get; set; }

        public BeneficiaryDetailsModel BeneficiaryDetails { get; set; }

        public OrderingPartyDetailsModel OrderingPartyDetails { get; set; }

    }
}