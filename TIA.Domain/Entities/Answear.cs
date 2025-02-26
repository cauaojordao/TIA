using TIA.Domain.Common;

namespace TIA.Domain.Entities
{
    public class Answear : BaseEntity
    {
        public Guid QuestionId { get; set; }
        public Question Question { get; set; } = null!;
        public string Text { get; set; } = string.Empty;
        public bool IsCorrect { get; set; }
    }
}
