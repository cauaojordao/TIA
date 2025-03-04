using TIA.Domain.Common;

namespace TIA.Domain.Entities
{
    public sealed class User : BaseEntity
    {
        public string Username { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public ICollection<AppFile> Files { get; set; } = new List<AppFile>();
    }
}
