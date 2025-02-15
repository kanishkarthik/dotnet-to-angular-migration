using DotNetApp.ViewModels.Base;
using DotNetApp.ViewModels.NAM.US.BKT;

namespace Application.ViewModels.NAM.US.BKT
{
    public class USBKTModel : BaseAppModel
    {
        public PaymentDetailsModel PaymentDetails { get; set; }

        public BeneficiaryDetailsModel BeneficiaryDetails { get; set; }

        public OrderingPartyDetailsModel OrderingPartyDetails { get; set; }


    }
}