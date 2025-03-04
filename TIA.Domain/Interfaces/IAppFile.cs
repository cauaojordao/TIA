using TIA.Domain.Entities;

namespace TIA.Domain.Interfaces
{
    public interface IAppFile
    {
        Guid UserId { get; set; }
        User User { get; set; }
        string? Folder { get; set; }
        string Name { get; set; }
        string Summary { get; set; }
        ICollection<Question> Questions { get; set; }
        decimal Efficiency { get; set; }
    }
}
