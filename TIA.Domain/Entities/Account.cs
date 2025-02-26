using TIA.Domain.Common;

namespace TIA.Domain.Entities
{
    public sealed class Account : BaseEntity
    {
        public string Username { get; set; } = string.Empty;
        public string UserEmail { get; set; } = string.Empty;
        public string UserRole { get; set; } = string.Empty;
        public ICollection<AppFile>? Files { get; set; } = new List<AppFile>();
    }
}
